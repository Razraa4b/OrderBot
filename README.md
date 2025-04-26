# OrderBot project
This project represents my small way to get orders on various freelance exchanges the fastest way to respond as one of the first people.

## Configuration

Before you can use the bot, you need to configure important details. In order for the bot to be able to work in telegram, a bot token is required, and connection strings to these services are needed to store data in the database and redis.

So you need to create an .env file with the contents of this template:
```bash
TOKEN="your_telegram_bot_token"
DB_CONNECTION_STRING="mysql+aiomysql://user:pass@host:port/database"
```

## Installation

It remains to download the necessary dependencies in the form of packages for the bot to work. It is desirable to create a virtual environment to avoid clogging your system with a lot of packages.

To install them, go to the root folder of the project and use the command:
```bash
pip install -r requirements.txt
```

## Usage
> [!WARNING]
> You need to find the *.env configuration file in the root folder of the project for the bot to find the *.env configuration file.
Now that we are fully prepared, we can launch the bot using the command:
```
python src/main.py
```

