from imports import *
from func import *
from config import *

def in_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 В меню", callback_data="in_menu"))
    return keyboard

def menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🛒 Купить логи", callback_data="buy_logs"),
        InlineKeyboardButton("👤 Мой профиль", callback_data="profile"),
        InlineKeyboardButton("🛠 Тех. поддержка", callback_data="support")
    )
    
    return keyboard

def toprep(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💵 Пополнить", callback_data="topup"),
        InlineKeyboardButton("🔙 В меню", callback_data="in_menu")
    )
    return keyboard

def cpm():
    cpmkeyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="💠 Crypto bot", callback_data="crypto_bot")
    button2 = InlineKeyboardButton(text="💰 Lolzteam", callback_data="lolzteam_market")
    button3 = InlineKeyboardButton("🔙 В меню", callback_data="in_menu")
    cpmkeyboard.add(button1, button2, button3)
    return cpmkeyboard
    # Я спиздил из одного моего проекта этую функцию, поэтому тут добавление не как у всех

def buy(log_type):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💳 Купить", callback_data=f"buy:{log_type}"),
        InlineKeyboardButton("🔙 В меню", callback_data="in_menu")
    )
    return keyboard

def logstype():
    prices = cfprices()
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(f"📁 Логи ({prices['logs']} RUB)", callback_data="log_type:logs"),
        InlineKeyboardButton(f"💎 Премиум логи ({prices['premium_logs']} RUB)", callback_data="log_type:premium_logs"),
        InlineKeyboardButton("🔙 В меню", callback_data="in_menu")
    )
    return keyboard