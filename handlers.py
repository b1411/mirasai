from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from redis import Redis
import assistant
import json
import time

router = Router()

r = Redis(host='https://services-jasik.alwaysdata.net', port=8300, db=0)


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Ты начал сессию с MIRAS AI. Напиши сообщение, и я отвечу на него.')


@router.message(F.text)
async def message_handler(msg: Message):
    contact = msg.from_user.id

    if r.get(contact):
        data = json.loads(r.get(contact))
    if data != None:
        data['timestamp'] = time.time()

    r.set(contact, json.dumps(data))

    if time.time() - data['timestamp'] > 300:
        r.delete(contact)
        await msg.answer('Сессия завершена. Начните снова.')

    await msg.answer(assistant.get_response(msg.text, contact, r))


@router.message(F.text & Command('help'))
async def help_handler(msg: Message):
    await msg.answer('Я - MIRAS AI. Напиши мне сообщение, и я отвечу на него.')


@router.message(F.voice)
async def voice_handler(msg: Message):
    await msg.answer("Я не понимаю голосовые сообщения. Пожалуйста, напиши мне.")
