from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from aiogram.fsm.state import State, StatesGroup

# Машина состояний 
class Data_collection(StatesGroup):
    statr = State()
    dates = State()
    times = State()
    another = State()
    

#Класс конфигурации для подгрузки данных из .env
class Config(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(env_file='bot/.env', env_file_encoding='utf-8')

# Инициализируем класс Config
config = Config()

# TODO временный список времён (нужно сделать выборку из таблицы)
time_dict = [
    "10:00-14:00",
    "12:00-16:00",
    "14:00-18:00",
    "16:00-20:00",
    "18:00-22:00",
    "20:00-00:00"
]
