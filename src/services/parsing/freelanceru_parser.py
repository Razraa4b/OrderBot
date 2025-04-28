from typing import List
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from .parser import Parser
from .order import Order


class FreelanceruParser(Parser[List[Order]]):
    async def parse(self) -> List[Order]:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://freelance.ru/project/search") as response:
                content = await response.text()
                soup = BeautifulSoup(content, features="lxml")

                projects = soup.select('div.project:not(.highlight)')
                orders = []
                for project in projects:
                    try:
                        title = project.select("h2.title")[0]
                        link = "https://freelance.ru" + str(title.find("a")["href"])
                        publish_time = str(project.select("div.publish-time")[0]["title"])
                        order = Order(title.getText(), link, self.parse_datetime(publish_time))
                        orders.append(order)
                    except IndexError:
                        continue
                return orders
    
    def parse_datetime(self, s: str) -> datetime | None:
        # example: "2025-04-26 в 19:13"
        return datetime.strptime(s, "%Y-%m-%d в %H:%M")
