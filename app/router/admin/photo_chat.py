from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from typing import List, Dict
import asyncio
from datetime import datetime

from sqlalchemy.orm import joinedload

from app.core.database import AsyncSessionLocal
import os
from app.core.create_bot import bot
from app.models import User
from app.repositories import user_repository

load_dotenv()

photo_chat_all_router = Router()

media_groups: Dict[str, List[types.Message]] = {}


class WaitForMessage(StatesGroup):
    waiting = State()


@photo_chat_all_router.message(Command("photoAll"))
async def message_chat(message: types.Message, state: FSMContext):
    YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")
    YOUR_CHAT_ID = int(YOUR_CHAT_ID)

    if message.chat.id == YOUR_CHAT_ID:
        await state.set_state(WaitForMessage.waiting)
        await message.reply(
            "Отправь фото (можно несколько), оно отправится всем. Напиши /stop когда закончишь."
        )
    else:
        await message.reply("Соси")


@photo_chat_all_router.message(WaitForMessage.waiting, F.media_group_id)
async def handle_media_group(message: types.Message, state: FSMContext):
    media_group_id = message.media_group_id

    if media_group_id not in media_groups:
        media_groups[media_group_id] = []
        asyncio.create_task(process_media_group_with_delay(media_group_id, state))

    if not any(
        msg.message_id == message.message_id for msg in media_groups[media_group_id]
    ):
        media_groups[media_group_id].append(message)


async def process_media_group_with_delay(media_group_id: str, state: FSMContext):
    await asyncio.sleep(3)

    if media_group_id in media_groups:
        messages = media_groups[media_group_id]
        if messages:
            caption = messages[0].caption if messages else None
            await process_and_send_photos(messages, caption, state)
            del media_groups[media_group_id]


@photo_chat_all_router.message(WaitForMessage.waiting, F.photo)
async def handle_single_photo(message: types.Message, state: FSMContext):
    if message.caption and message.caption.strip() == "/stop":
        await message.reply("Остановлено")
        await state.clear()
        media_groups.clear()
        return

    if message.media_group_id:
        return

    await process_and_send_photos([message], message.caption, state)


async def process_and_send_photos(
    messages: List[types.Message], caption: str, state: FSMContext
):
    try:
        if messages:
            await messages[0].reply(f"Получил {len(messages)} фото")

        photos_data = []
        for msg in messages:
            if msg.photo:
                photo = msg.photo[-1]
                file = await bot.download(photo)
                photo_bytes = file.read()
                photos_data.append(
                    {
                        "bytes": photo_bytes,
                        "caption": caption if len(photos_data) == 0 else None,
                    }
                )

        if not photos_data:
            if messages:
                await messages[0].reply("Не найдено фотографий для отправки")
            await state.clear()
            return

        async with AsyncSessionLocal() as session:
            users = await user_repository.get_all(
                session,
                filter_criteria=User.is_active,
                custom_options=(joinedload(User.balance),),
            )

            successful_sends = 0
            for user in users:
                try:
                    if len(photos_data) == 1:
                        await bot.send_photo(
                            chat_id=user.chat_id,
                            photo=types.BufferedInputFile(
                                photos_data[0]["bytes"],
                                filename=f"photo_{user.group_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                            ),
                            caption=photos_data[0]["caption"],
                        )
                    else:
                        media = []
                        for i, photo_data in enumerate(photos_data):
                            media_item = types.InputMediaPhoto(
                                media=types.BufferedInputFile(
                                    photo_data["bytes"],
                                    filename=f"photo_{user.group_name}_{i + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                                ),
                                caption=photo_data["caption"] if i == 0 else None,
                            )
                            media.append(media_item)

                        await bot.send_media_group(chat_id=user.chat_id, media=media)

                    successful_sends += 1
                    print(
                        f"Успешно отправлено {len(photos_data)} фото в {user.group_name}"
                    )

                except Exception as e:
                    print(f"Ошибка при отправке фото для {user.group_name}: {str(e)}")

            if successful_sends > 0:
                await messages[0].reply(
                    f"Отправлено {len(photos_data)} фото в {successful_sends} групп"
                )

    except Exception as e:
        print(f"Общая ошибка: {str(e)}")
        if messages:
            await messages[0].reply(f"Произошла ошибка: {str(e)}")


@photo_chat_all_router.message(WaitForMessage.waiting)
async def handle_other_messages(message: types.Message, state: FSMContext):
    if message.text and message.text.strip() == "/stop":
        await message.reply("Остановлено")
        await state.clear()
        media_groups.clear()
    else:
        await message.reply("Отправь фотографии или напиши /stop для отмены")


async def setup_photo_router(dp):
    media_groups.clear()
