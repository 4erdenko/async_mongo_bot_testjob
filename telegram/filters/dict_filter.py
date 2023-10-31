import json

from aiogram.filters import Filter
from aiogram.types import Message


class IsJSONWithFields(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            data = json.loads(message.text)
            if not isinstance(data, dict):
                return False
            return all(
                field in data for field in ['dt_from', 'dt_upto', 'group_type']
            )
        except json.JSONDecodeError:
            return False
