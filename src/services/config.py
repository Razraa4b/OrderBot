from os import getenv
from dotenv import load_dotenv


class Configuration:
    def __init__(self) -> None:
        load_dotenv()

        self._token = getenv("TOKEN")
        self._db_connection_string = getenv("DB_CONNECTION_STRING")
        self._redis_url = getenv("REDIS_URL")

    def get_token(self) -> str | None:
        return self._token
    
    def get_db_connection_string(self) -> str | None:
        return self._db_connection_string
    
    def get_redis_url(self) -> str | None:
        return self._redis_url
