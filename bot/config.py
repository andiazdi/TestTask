from dotenv import load_dotenv
from os import environ

load_dotenv()

# TELEGRAM_TOKEN = environ.get("TELEGRAM_TOKEN")
# POSTGRES_URL = environ.get("POSTGRES_URL")
# REQUIRED_CHANNELS = {"Канал тестовое задание": environ.get("REQUIRED_CHANNELS")}
# REQUIRED_CHATS = {"Чат тестовое задание": environ.get("REQUIRED_CHATS")}
# PAYMENT_TOKEN = environ.get("PAYMENT_TOKEN")

TELEGRAM_TOKEN = "8057093341:AAGMUf2gVUnykOQSFQhpH_oYJZsHi-wa_5o"
POSTGRES_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_task"
REQUIRED_CHANNELS = {"Канал тестовое задание": "@dasdfasjkfasj"}
REQUIRED_CHATS = {"Чат тестовое задание": "@sadasdasdazxcz"}
PAYMENT_TOKEN = "381764678:TEST:125448"
