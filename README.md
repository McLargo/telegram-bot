# Telegram Bot

This small application creates a Telegram bot that can respond to commands sent
via Telegram messages. The ideas is that this bot can be executed as a daemon in
your Raspberry Pi, so you can send commands to your Raspberry Pi from anywhere
using Telegram.

## Configuration

Before anything, we need to create a new bot in Telegram by talking to the
[@BotFather](https://t.me/BotFather). After bot is created, get the token and
keep it safe.

## Installation and debugging

First, create a virtual environment and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> NOTE: If you are using a old version of Raspberry Pi, you may need to specify
> the Python version you are using, by adding suffix 3 to python/pip commands.
> Also, make sure pip and venv are installed. You can install them with:

```bash
sudo apt install python3-pip python3-venv
pip3 install virtualenv
python3 -m virtualenv .venv
...
```

Now, you can run the bot with the following command, replacing
`your_bot_token_here` with the token you got from BotFather:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
python -m main
```

To run the bot in debug mode with more verbose output, set the debug variable:

```bash
export TELEGRAM_BOT_DEBUG="1"
```

After running the bot, you should see a notification in Telegram that your bot
is online. You can now send messages to your bot for testing.

## Daemon creation

WIP

## Supervisor configuration

WIP

## References

- [Python library](https://python-telegram-bot.org/)
