from aiogram import Router

from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data import Data_collection

from utils.gpt_reader import extract_data_with_ai

router = Router()

@router.message(Command("redact"))
async def redact_text_with_ai(msg: Message, state: FSMContext):
    await msg.answer("Введите сообщения для обработки:")
    await state.set_state(Data_collection.redact_text)


@router.message(StateFilter(Data_collection.redact_text))
async def redact_teble_with_ai(msg: Message):
    data = await extract_data_with_ai(msg.text)

    await msg.answer("".join(data))
