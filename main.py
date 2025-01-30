from imports import *
from config import *
from buttons import *
from func import *
from dbclass import *

@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    user_id = message.from_user.id
    c.execute("SELECT accept FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result and result[0] == 1:
        keyboard = menu()
        await message.answer("👋 Добро пожаловать!", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        accept_button = InlineKeyboardButton(text="✅ Я согласен", callback_data="accept")
        keyboard.add(accept_button)
        await message.answer(
            f"Нажимая кнопку ниже, вы соглашаетесь с нашей <a href='{linkonpol}'>политикой и правилами использования</a>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'accept')
async def process_accept(callback_query):
    user_id = callback_query.from_user.id
    c.execute("UPDATE users SET accept = 1 WHERE user_id = ?", (user_id,))
    conn.commit()

    keyboard = menu()
    await bot.send_message(user_id, "👋 Добро пожаловать!", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "buy_logs")
async def process_buy_logs(call: CallbackQuery):
    prices = cfprices()
    keyboard = logstype()
    await bot.edit_message_text("📂 Выберите тип логов:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("log_type:"))
async def process_log_type(call: CallbackQuery):
    log_type = call.data.split(":")[1]
    prices = cfprices()
    price = prices[log_type]
    
    keyboard = buy(log_type)
    
    text = f"📀 {log_type.replace('_', ' ').title()}\n1 файл = {price} RUB\n"
    
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("buy:"))
async def process_purchase(call: CallbackQuery):
    user_id = call.from_user.id
    log_type = call.data.split(":")[1]
    prices = cfprices()
    price = prices[log_type]
    
    if get_balance(user_id) < price:
        await bot.answer_callback_query(call.id, "❌ Недостаточно средств на балансе!")
        return
    
    source_folder = log_type
    files = os.listdir(source_folder)
    if not files:
        await bot.answer_callback_query(call.id, "⚠️ Логи этого типа временно отсутствуют!")
        return
    
    selected_file = random.choice(files)
    dest_folder = "otrabot_logs"
    
    os.makedirs(dest_folder, exist_ok=True)
    shutil.move(os.path.join(source_folder, selected_file), os.path.join(dest_folder, selected_file))
    
    update_balance(user_id, -price)
    
    if delete_otrabot:
        os.remove(os.path.join(dest_folder, selected_file))
    
    await bot.send_document(user_id, open(os.path.join(dest_folder, selected_file), "rb"), 
                           caption=f"✅ Успешная покупка! Файл: {selected_file}")

@dp.callback_query_handler(lambda c: c.data == "profile")
async def process_profile(call: CallbackQuery):
    user_id = call.from_user.id
    balance = get_balance(user_id)
    text = f"🆔 Ваш ID: {user_id}\n💰 Баланс: {balance} RUB"
    keyboard = toprep(user_id)
    await call.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

@dp.callback_query_handler(lambda c: c.data == "support")
async def process_support(call: CallbackQuery):
    support_list = "\n".join([f"• {username}" for username in tp_list()])
    keyboard = in_menu()
    await call.message.edit_text(f"🛎  агенты поддержки:\n{support_list}", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "topup")
async def topup(call: CallbackQuery):
    await call.message.edit_text("Выберите метод пополнения:", reply_markup=cpm())

@dp.callback_query_handler(lambda c: c.data == "crypto_bot")
async def cryptobotopup(call: CallbackQuery):
    user_id = call.from_user.id
    keyboard = in_menu()
    await call.message.edit_text(f"Введите сумму для пополнения (в RUB):", reply_markup=keyboard)
    await dp.current_state(user=user_id).set_state("waiting_amount")

@dp.message_handler(lambda message: message.text.isdigit(), state="waiting_amount")
async def enter_amount(message: Message):
    try:
        amount_rub = int(message.text)
        if 10 <= amount_rub <= 100000:
            user_id = message.from_user.id
            await dp.current_state(user=user_id).finish()
            usdt_amount = await convert_to_usdt(amount_rub)
            invoice = await crypto_client.create_invoice(asset="USDT", amount=usdt_amount)
            burl1 = await burl(invoice)
            await message.answer(f"💳 Пополните баланс в течении 5 минут на {usdt_amount} USDT по кнопке ниже:", reply_markup=burl1)
            await check_payment(user_id, invoice.invoice_id, amount_rub)
        else:
            await message.reply("❗ Введите сумму больше чем 10 рублей и меньше чем 100 000!")
    except Exception as e:
    	await message.reply(f"Ошибка: {e}")

@dp.callback_query_handler(lambda c: c.data == "in_menu", state="*")
async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    keyboard = menu()
    await call.message.edit_text("👋 Добро пожаловать!", reply_markup=keyboard)

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp, skip_updates=True)