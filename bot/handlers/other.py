from aiogram import Router

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

from utils import Dates, DataExtractor
from data import Data_collection

from utils.kb_builder import create_kb
from data.config_reader import time_dict


router = Router()
extraktor = DataExtractor("Couriers_scheduls")

# Команда старт
@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    kb = ReplyKeyboardBuilder()
    kb.max_width = 1

    kb.button(text=f"{Dates.today()[0]}")
    kb.button(text=f"{Dates.tomorrow_day()[0]}")
    kb.button(text=f"{Dates.after_tomorrow_day()[0]}")
    kb.button(text="Другой день")

    await msg.answer(
        f"Выберите день:", 
        reply_markup = kb.as_markup(resize_keyboard=True)
    )
    await state.set_state(Data_collection.dates)

# Функция выбора или фильтрации даты 
@router.message(StateFilter(Data_collection.dates))
async def dates_func(msg: Message, state: FSMContext):
    # Выбор даты вручную
    if msg.text == "Другой день":
        await msg.answer("Введите дату в формате ДД-ММ-ГГГГ")
        await state.set_state(Data_collection.another)

    # Выбор даты по кнопкам
    elif msg.text == Dates.today()[0] or Dates.tomorrow_day()[0] or Dates.after_tomorrow_day()[0]:
        
        if msg.text == Dates.today()[0]:
            await state.update_data(dates=Dates.today()[1])

        elif msg.text == Dates.tomorrow_day()[0]:
            await state.update_data(dates=Dates.tomorrow_day()[1])

        elif msg.text == Dates.after_tomorrow_day()[0]:
            await state.update_data(dates=Dates.after_tomorrow_day()[1])

        await msg.answer(
            "Выберите временной период",
            reply_markup=create_kb(2, *time_dict)
        )
        await state.set_state(Data_collection.times)

    # Если пользователь ввёл что-то другое
    else:
        await msg.answer("Такого варианта я не знаю")

# Функция выбора времени
@router.message(StateFilter(Data_collection.another))
async def another_date(msg: Message, state: FSMContext):
    await state.update_data(dates=msg.text)

    await msg.answer(
    "Выберите временной период",
    reply_markup=create_kb(2, *time_dict)
    )

    await state.set_state(Data_collection.times)

# Функция отправки всех данных 
@router.message(StateFilter(Data_collection.times))
async def times_func(msg: Message, state: FSMContext):
    await state.update_data(times=msg.text)

    # Сохранение данных в словарь
    date_dict = await state.get_data()
    
    await state.clear()

    # Выборка данных из гугл таблиц
    data_list = extraktor.extract_data("расписание", date_dict["dates"], date_dict["times"])
    another_data = extraktor.find_data_another_sheet(data_list, "курьеры")
   
    # Получение имён пользователей телеграмм
    tg_links_list = []
    for sublist in another_data:
        try:
            tg_links_list.append(sublist[0])
        except:
            tg_links_list.append('')

    # Получение номеров телефона 
    numbers = []
    for sublist in another_data:
        try:
            numbers.append(sublist[1])
        except:
            numbers.append('')

    # Фильтрация и сбор данных
    share = []
    for mess, links, number in zip(data_list, tg_links_list, numbers):
        if links != '':
            message = f"<a href='t.me/{links}'>{mess}</a>"
            share.append(message)
        elif links == '' and number != '':
            message = f"{mess}  {number}"
            share.append(message)
        else:
            message = f"{mess} нету тг и номера ("
            share.append(message)

    # Отправка даты и времени
    await msg.answer(
        "Вы выбрали:\n"
        f"Дата: {Dates.transfomation(date_dict['dates'])}\n"
        f"Время: {date_dict['times']}\n",
        reply_markup=ReplyKeyboardRemove()
        )
    
    # Отправка имен курьеров с сылками или номерами
    await msg.answer(
        "\n".join(share),
        disable_web_page_preview=True
        )
