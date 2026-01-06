from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import joinedload

from app.core.database import AsyncSessionLocal
import os
from dotenv import load_dotenv

from app.core.create_bot import bot
from app.models import User
from app.repositories import user_repository

load_dotenv()

message_chat_all_router = Router()


class WaitForMessage(StatesGroup):
    waiting = State()


@message_chat_all_router.message(Command("messageAll"))
async def message_chat(message: types.Message, state: FSMContext):
    YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")
    YOUR_CHAT_ID = int(YOUR_CHAT_ID)

    if message.chat.id == YOUR_CHAT_ID:
        await state.set_state(WaitForMessage.waiting)
        await message.reply("Ну давай кобылка, пиши сообщение, оно отправитя всем:")

    else:
        await message.reply("Соси")


@message_chat_all_router.message(WaitForMessage.waiting, F.text)
async def handle_next_message(message: types.Message, state: FSMContext):
    user_message = message.text
    if user_message == "/stop":
        await message.reply("Щегол")
        await state.clear()
    else:
        await message.reply("Щаааа")
        try:
            async with AsyncSessionLocal() as session:
                users = await user_repository.get_all(
                    session,
                    filter_criteria=User.is_active,
                    custom_options=(joinedload(User.balance),),
                )
                for user in users:
                    try:
                        await bot.send_message(user.chat_id, user_message)
                        print(
                            f"Сообщение пользователю из {user.group_name} отправлено в чат {user.chat_id}."
                        )
                    except Exception as e:
                        print(
                            f"Ошибка при отправке сообщения для группы {user.group_name}: {e}"
                        )
        except Exception as e:
            print(f"Ошибка при получении данных из базы: {e}")
        await state.clear()
