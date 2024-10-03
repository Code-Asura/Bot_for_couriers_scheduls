from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Coздание клавиатуры
def create_kb(width: int, *args: str, **kwargs: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []

    # Распаковка списков
    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))

    # Распаковка словарей
    if kwargs:
        for key, val in kwargs.items():
            buttons.append(KeyboardButton(text=val))

    kb.row(*buttons, width=width)

    return kb.as_markup(resize_keyboard=True)
