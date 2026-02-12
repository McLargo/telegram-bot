# User stories

Professionally, I work with a defined User Story Template. Focus on the value
that provides to the user and not focus on the technical details.You can see the
template below:

```text
As a (type of user),
I want to (perform some action),
so that (achieve some goal).
```

First line is focus on who is doing the action, second line is focus on what
they want and third line is the why they want it.

So, following the template, my first user story for this project is:

```text
As a developer,
I want to have a place where I can put the user stories required,
so that I can define the requirements before start working on them
and have a clear vision of the project.
```

Let's go with the core user story of the project:

```text
As a user,
I want to talk to my Raspberry Pi from my mobile phone,
so that I can connect it from anywhere
and send commands to receive notification directly from Raspberry Pi.
```

Being said that, we can split into smaller user stories, grouped in different
categories.

## Technical (As a developer)

```text
As a developer,
I want to create a Telegram bot
so that it can respond to commands sent via Telegram.
```

```text
As a developer,
I want to stop the service if another instance is already running
so that only one service is online at the time.
```

```text
As a developer,
I want to run the service as a daemon in my Raspberry Pi
so that every time my Raspberry Pi the service starts automatically
and the bot is online and ready to accept messages.
```

```text
As a developer,
I want to have a debug mode with more verbose output
so that I can troubleshoot issues more effectively
and avoid sending notification to the user.
```

## Functionality (As a user)

```text
As a user,
I want to receive a notification on service start up to my Telegram chat
so that I know the bot is online and ready to accept messages.
```

```text
As a user,
I want to receive a notification on service stop to my Telegram chat
so that I know th bot is offline.
```

```text
As a user,
I want to receive a notification to my Telegram chat when `/hello` command is send
so that I know who I am.
```

```text
As a allowed user,
I want to reboot my Raspberry Pi when `/reboot` command is send
and receive a notification to my Telegram chat when the command is executed
so that I can reboot my Raspberry Pi from my phone.
```

```text
As a not allowed user,
I want to receive a forbidden notification when `/reboot` command is send
and log the attempt in the logs
so that I know I am not allowed to reboot the Raspberry Pi
```
