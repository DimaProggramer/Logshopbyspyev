from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
import aiohttp
import re
import random
import time
import shutil
from aiogram.utils import executor
from aiocryptopay import AioCryptoPay, Networks
from aiogram.types import CallbackQuery, Message, ParseMode, ContentType
import asyncio
import sqlite3
import os
import os
from datetime import datetime, timedelta
import json
# from lolzteam_payment import *