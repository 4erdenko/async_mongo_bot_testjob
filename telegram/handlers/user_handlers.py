import json

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from aggregator.aggregation_algorithms import SalaryAggregator
from database.db import MongoBase
from telegram.filters.dict_filter import IsJSONWithFields
from telegram.lexicon.lexicon_ru import LEXICON_RU

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'], disable_web_page_preview=True
    )


@router.message(IsJSONWithFields())
async def handle_json_message(message: Message):
    data = json.loads(message.text)
    aggregator = SalaryAggregator(data)
    db = MongoBase()
    result = await aggregator.aggregate(db)
    return await message.answer(str(result))
