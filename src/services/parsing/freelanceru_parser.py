from typing import List

import aiohttp
from bs4 import BeautifulSoup

from .parser import Parser
from .order import Order


class FreelanceruParser(Parser[List[Order]]):
    async def parse() -> List[Order]:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://freelance.ru/project/search") as response:
                content = await response.text()
                soup = BeautifulSoup(content, features="lxml")

                projects = soup.select('div.project:not(.highlight)')
                orders = []
                for project in projects:
                    title = project.find("h2", class_=".title")
                    link = str(title.find("a")["href"])
                    publish_time = str(project.find("div", class_="publish-time")["title"])
                    
                    order = Order(title.text(), link, publish_time)
                    order.append(order)
                return orders 
