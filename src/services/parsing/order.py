from datetime import datetime


class Order:
    def __init__(self, title: str, link: str, publish_time: datetime) -> None:
        self.title = title
        self.link = link
        self.publish_time = publish_time
