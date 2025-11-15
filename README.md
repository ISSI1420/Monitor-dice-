# Telegram 777 Dice Monitor — Advanced Interactive Bot

This project is an advanced Telethon-based monitoring bot that tracks Telegram dice rolls, detects the jackpot value (default: 64), records user hit history, and sends HTML notifications with clickable inline buttons for each hit message.

The bot is designed for reliable production deployment on:
- Termux (Android)
- Docker and Docker Compose
- Linux VPS
- Render.com (Docker deployment)
- Windows (CMD or PowerShell)

---

## Features

- Detects dice value 64 in selected chats.
- Tracks hit counts for each user with automatic persistence.
- Sends HTML notifications with dynamic inline buttons linked to message URLs.
- Full template customization through settings.json.
- Stores user hit history in user_hits.json.
- Built-in interactive CLI:
  - add @chat
  - remove @chat
  - list
  - preview partial
  - preview winner
  - quit

---

## Project Structure
telegram-777-monitor/ ├─ interactive_monitor_777_with_buttons.py ├─ settings.json ├─ requirements.txt ├─ .env.example ├─ Dockerfile ├─ docker-compose.yml ├─ user_hits.json ├─ LICENSE └─ README.md

---

## Environment Configuration

Create a `.env` file based on `.env.example`:

API_ID=123456 API_HASH=your_api_hash_here STRING_SESSION= SESSION_NAME=monitor_session RESULTS_ACCOUNT=@YourResultsChannel

Generate a String Session:

python3 -m telethon.sessions

---

## Running on Linux / VPS

sudo apt update sudo apt install python3 python3-pip -y pip3 install -r requirements.txt python3 interactive_monitor_777_with_buttons.py

---

## Running on Termux (Android)

pkg update pkg install python git -y pip install --upgrade pip git clone https://github.com/yourname/telegram-777-monitor cd telegram-777-monitor pip install -r requirements.txt python interactive_monitor_777_with_buttons.py

---

## Running with Docker

Build the image:

docker build -t telegram-777-monitor .

Run the container:

docker run --env-file .env telegram-777-monitor

---

## Running with Docker Compose

docker compose up -d

This keeps the bot running in the background and automatically restarts it.

---

## Deploying on Render.com (Docker Deployment)

1. Push the project to GitHub.
2. Create a new "Web Service" on Render.
3. Choose "Docker" as the environment.
4. Add all `.env` variables in Render's Environment Configuration.
5. Deploy.

Render will automatically build the Docker image from your Dockerfile.

---

## Running on Windows (CMD / PowerShell)

Install dependencies:

pip install -r requirements.txt python interactive_monitor_777_with_buttons.py

Run in background:

Start-Job -ScriptBlock { python interactive_monitor_777_with_buttons.py }

---

## Target Chat Management (Interactive CLI)

add @NewChat remove @OldChat list preview partial preview winner quit

---

## Auto-Restart on Linux (systemd)

Create and edit:

nano /etc/systemd/system/telegram-monitor.service

Add:

[Unit] Description=Telegram 777 Monitor After=network.target

[Service] WorkingDirectory=/root/telegram-777-monitor ExecStart=/usr/bin/python3 interactive_monitor_777_with_buttons.py Restart=always

[Install] WantedBy=multi-user.target

Enable:

systemctl enable telegram-monitor systemctl start telegram-monitor

---

## Credits

Developed by @TON50B
