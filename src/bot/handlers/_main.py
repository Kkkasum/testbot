import json
from datetime import datetime

from aiogram import Router, types

from src.database import db


router = Router()


@router.message()
async def start(message: types.Message):
    try:
        data = json.loads(message.text)
        dt_from, dt_upto = datetime.fromisoformat(data['dt_from']), datetime.fromisoformat(data['dt_upto'])
        group_type = data['group_type']

        labels = db.get_labels(dt_from, dt_upto, group_type)
        dataset = await db.get_dataset(dt_from, dt_upto, group_type, labels)

        m = str({'dataset': dataset, 'labels': labels}).replace('\'', '\"')
        await message.answer(text=m)
    except json.decoder.JSONDecodeError:
        await message.answer(text='Введите правильный формат данных')
