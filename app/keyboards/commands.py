from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(command="getbalance", description="Узнать свой баланс"),
        BotCommand(command="play", description="Начать игру"),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
