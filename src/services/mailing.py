from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode

from services.database.context import DatabaseContext
from services.database.models import User

from services.parsing import FreelanceruParser, Order


async def send_mail(bot: Bot, user: User, new_orders: List[Order]) -> None:
    if len(new_orders) == 0:
        return
    
    message = ""
    # building message
    for order in new_orders:
        message += f"<b><a href=\"{order.link}\">{order.title}</a></b>\n"

    await bot.send_message(chat_id=user.telegram_id, text=message, parse_mode=ParseMode.HTML)


async def start_mailing(bot: Bot, context: DatabaseContext | None) -> None:
    users: List[User] = await context.get_all(User, True, [User.bot_settings])

    # parsers
    parsers = [FreelanceruParser()]

    # parsing
    orders: List[Order] = []
    for parser in parsers:
        result = await parser.parse()
        orders += result

    now = datetime.now()
    
    new_orders: List[Order] = []
    for order in orders:
        diff = relativedelta(now, order.publish_time)
        print(diff)
        if (diff.minutes < 15 and
            diff.hours == 0 and
            diff.days == 0 and
            diff.months == 0 and
            diff.years == 0):
            new_orders.append(order)
        else:
            continue

    # sending mails
    tasks = []
    for user in users:
        if user.bot_settings.is_enabled:
            tasks.append(asyncio.create_task(send_mail(bot, user, new_orders)))
    await asyncio.gather(*tasks)
