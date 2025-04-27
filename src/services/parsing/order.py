from datetime import datetime


class Order:
    def __init__(self, title: str, link: str, publish_time: datetime) -> None:
        self.title = title
        self.link = link
        self.publish_time = publish_time

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Order):
            return self.link == obj.link
        else:
            return False
