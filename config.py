from imports import *

API_TOKEN = ""
CRYPTO_TOKEN = ""

delete_otrabot = False
linkonpol = "https://huy.com"

storage = MemoryStorage()
crypto_client = AioCryptoPay(CRYPTO_TOKEN, network=Networks.MAIN_NET)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)