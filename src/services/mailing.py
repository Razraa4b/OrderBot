from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode

from services.database.context import DatabaseContext
from services.database.models import User
from services.parsing import FreelanceruParser, Order
from services.redis import Redis


async def send_mail(bot: Bot, redis: Redis, user: User, new_orders: List[Order]) -> None:
    if len(new_orders) == 0:
        return
    
    message = ""

    viewed_orders = await redis.lrange(user.telegram_id, 0, -1)
    # building message
    for order in new_orders:
        if order.link not in list(map(lambda l: l.decode("utf-8"), viewed_orders)):
            await redis.push(user.telegram_id, 901, order.link)
            message += f"<b><a href=\"{order.link}\">{order.title}</a></b>\n"

    if message:
        await bot.send_message(chat_id=user.telegram_id, text=message, parse_mode=ParseMode.HTML)


async def start_mailing(bot: Bot, context: DatabaseContext | None, redis: Redis) -> None:
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
        # check the difference in the time of publication, if it is out of date, do not put on new orders
        diff = relativedelta(now, order.publish_time)
        if (diff.minutes < 30 and
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
            tasks.append(asyncio.create_task(send_mail(bot, redis, user, new_orders)))
    await asyncio.gather(*tasks)
