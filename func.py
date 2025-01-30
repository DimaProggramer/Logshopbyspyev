from imports import *
from config import *
from dbclass import *

if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("premium_logs"):
    os.makedirs("premium_logs")
if not os.path.exists("otrabot_logs"):
    os.makedirs("otrabot_logs")

class Form(StatesGroup):
    waiting_for_amount = State()
    waiting_lolzteam_amount = State()
    waiting_for_broadcast = State()
def cfprices():
    with open("price.json", "r") as f:
        return json.load(f)

def tp_list():
    with open("tp.json", "r") as f:
        return json.load(f).values()

def parse_inline_buttons(text):
    inline_pattern = r'\[inline_text="(.*?)"_url="(.*?)"\]'
    matches = re.findall(inline_pattern, text)

    if matches:
        buttons = []
        for match in matches:
            button_text, button_url = match
            buttons.append(InlineKeyboardButton(text=button_text, url=button_url))
        text_without_buttons = re.sub(inline_pattern, "", text).strip()
        return {
            "text": text_without_buttons,
            "buttons": InlineKeyboardMarkup(row_width=1).add(*buttons)
        }
    return {"text": text, "buttons": None}

async def burl(invoice):
    burlkeyboard = InlineKeyboardMarkup(row_width=1)
    buttonurl = InlineKeyboardButton(text="Оплатить", url=invoice.pay_url)
    inmenu = InlineKeyboardButton("🔙 В меню", callback_data="in_menu")
    burlkeyboard.add(buttonurl, inmenu)
    return burlkeyboard

async def convert_to_usdt(amount_rub):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub") as response:
            data = await response.json()
            rub_to_usdt_rate = data["tether"]["rub"]
    usdt_amount = amount_rub / rub_to_usdt_rate
    return round(usdt_amount, 2)

async def check_payment(user_id, invoice_id, amount_rub):
    for _ in range(60):
        await asyncio.sleep(5)
        try:
            invoices = await crypto_client.get_invoices(invoice_ids=[invoice_id])
            if invoices and invoices[0].status == "paid":
                update_balance(user_id, amount_rub)
                await bot.send_message(user_id, f"✅ Ваш баланс пополнен на {amount_rub} RUB!")
                return
        except Exception as e:
            print(f"Ошибка при проверке оплаты: {e}")
    await bot.send_message(user_id, "❌ Время оплаты истекло.")

async def check_payment_lolzteam(user_id, amount, comment):
    while True:
        is_paid = await lolzteam_client.check_status_payment(pay_amount=amount, comment=comment)
        if is_paid:
            update_balance(user_id, amount_rub)
            await bot.send_message(user_id, f"✅ Ваш баланс успешно пополнен на {amount} RUB!")
            break
        await asyncio.sleep(30)