# Telegram Bot

- [CONTRIBUTING.md](CONTRIBUTING.md)

This small application creates a Telegram bot that can respond to commands sent
via Telegram messages. The idea is that this bot can be executed as a daemon in
your Raspberry Pi, so you can send commands to your Raspberry Pi from anywhere
using Telegram.

You can find the more details of the use cases and requirements in the [use
stories](docs/user-stories.md) document.

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
export TELEGRAM_BOT_DEBUG="true"
```

After running the bot, you should see a notification in Telegram that your bot
is online. You can now send messages to your bot for testing.

## Daemon creation with systemd service

Copy the telegram-bot.service file to the systemd directory:

```bash
sudo cp telegram-bot.service /etc/systemd/system/telegram-bot.service
```

Or you can create a symbolic link:

```bash
sudo ln -s config/telegram-bot.service /etc/systemd/system/telegram-bot.service
```

Next step us is to reload the systemd manager configuration, so it recognizes
the new service:

```bash
sudo systemctl daemon-reload
```

You can enable the service to start on boot with the following command or run it
manually:

```bash
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

## Troubleshooting

To check the status of the service, use:

```bash
sudo systemctl status telegram-bot.service
```

To view the logs of the service, use:

```bash
sudo journalctl -u telegram-bot.service -f
```

## Environment variables

The bot uses the following environment variables for configuration:

| Name | Description | Mandatory | Default |
| ------ | ------------- | ----------- | --------- |
| `TELEGRAM_BOT_TOKEN` | The token for your Telegram bot | ✅ | - |
| `TELEGRAM_ADMIN_CHAT_ID` | The chat ID of the admin user | ❌ | - |
| `TELEGRAM_BOT_DEBUG` | Set to "true" to enable debug logging | ❌ | `false` |
| `KODI_IP` | The IP address of your Kodi instance | ❌ | `localhost` |
| `KODI_PORT` | The port number of your Kodi instance | ❌ | `8080` |
| `KODI_USERNAME` | The username for Kodi authentication | ❌ | - |
| `KODI_PASSWORD` | The password for Kodi authentication | ❌ | - |

## References

- [Telegram python library](https://python-telegram-bot.org/)
