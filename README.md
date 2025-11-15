# ًںژ° Telegram 777 Dice Monitor â€” Advanced Interactive Bot
A powerful and fully automated Telethon-based monitoring bot that tracks Telegram dice rolls, detects jackpot results (default: value **64**), records user hits, and sends dynamic HTML notifications with inline buttons linking to each hit message.

This bot is designed for production-grade deployments across:
- Termux (Android)
- Docker / Docker Compose
- Linux VPS
- Render.com (Docker Deploy)
- Windows (CMD / PowerShell)

## ًں“Œ Features
- ًںژ¯ Detects dice value **64** in selected chats.
- ًں§® Tracks hit counts per user with automatic persistence.
- ًں“¨ Sends rich notifications with dynamic inline buttons.
- ًں§° Fully customizable templates (settings.json).
- ًں—‚ Automatic storage of hit history (user_hits.json).
- ًں–¥ Interactive CLI:
  - `add @chat`
  - `remove @chat`
  - `list`
  - `preview partial`
  - `preview winner`
  - `quit`

## ًں“پ Project Structure
```
telegram-777-monitor/
â”œâ”€ interactive_monitor_777_with_buttons.py
â”œâ”€ settings.json
â”œâ”€ requirements.txt
â”œâ”€ .env.example
â”œâ”€ Dockerfile
â”œâ”€ docker-compose.yml
â”œâ”€ user_hits.json
â”œâ”€ LICENSE
â””â”€ README.md
```

## ًں”§ Environment Variables
Create a `.env` file:

```
API_ID=123456
API_HASH=xxxxxxxxxxxxxxxxxxxx
STRING_SESSION=
SESSION_NAME=monitor_session
RESULTS_ACCOUNT=@YourResultsChannel
```

Generate string session:
```
python3 -m telethon.sessions
```

## â–¶ Running on Linux / VPS
```
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
python3 interactive_monitor_777_with_buttons.py
```

## ًں“± Running on Termux
```
pkg update
pkg install python git -y
pip install --upgrade pip
git clone https://github.com/yourname/telegram-777-monitor
cd telegram-777-monitor
pip install -r requirements.txt
python interactive_monitor_777_with_buttons.py
```

## ًںگ‹ Running with Docker
```
docker build -t telegram-777-monitor .
docker run --env-file .env telegram-777-monitor
```

## ًںگ³ Docker Compose
```
docker compose up -d
```

## âکپ Deploy on Render.com
- Push repo to GitHub  
- Create Docker Web Service  
- Add `.env` values  
- Deploy  

## ًںھں Running on Windows
```
pip install -r requirements.txt
python interactive_monitor_777_with_buttons.py
```

Background:
```
Start-Job -ScriptBlock { python interactive_monitor_777_with_buttons.py }
```

## ًں§  Target Chats CLI
```
add @NewChat
remove @OldChat
list
preview partial
preview winner
```

## ًں›  Auto-Restart (systemd)
```
[Unit]
Description=Telegram 777 Monitor
After=network.target

[Service]
WorkingDirectory=/root/telegram-777-monitor
ExecStart=/usr/bin/python3 interactive_monitor_777_with_buttons.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## ًں‘‘ Credits
Developed by **@TON50B**
