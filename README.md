<!-- HEADER -->
<p align="center">
  <img src="https://img.icons8.com/fluency/96/dice.png" width="110"/>
</p>

<h1 align="center">🎰 Telegram 777 Dice Monitor</h1>
<h3 align="center">Advanced Telethon-Based Jackpot Detection Bot</h3>

<p align="center">
A premium, production-ready monitoring bot built with Telethon.  
Detects jackpot dice results (value 64), tracks user hits, and sends rich HTML notifications  
with dynamic inline buttons for every hit.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Framework-Telethon-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Maintainer-@TON50B-purple?style=for-the-badge">
</p>

---

# ⭐ Overview

The Telegram 777 Dice Monitor is a highly optimized bot that:

- Detects dice rolls in selected Telegram chats  
- Watches specifically for the jackpot value 64  
- Tracks the user’s progress until winning  
- Sends multi-button HTML notifications  
- Stores hit history permanently  
- Includes a live interactive command-line control panel  

Supports:
- Termux (Android)
- Linux VPS
- Docker & Docker Compose
- Render.com (Docker Deploy)
- Windows CMD/PowerShell

---

# ✨ Main Features

### 🎯 Jackpot Detection
Automatically identifies dice messages with value 64.

### 📊 Persistent Hit Tracking
Tracks and stores hits for every user across restarts.

### 📨 Dynamic Inline Buttons
Every hit gets its own button:
- Hit 1  
- Hit 2  
- Hit 3  

Each button opens the original Telegram message.

### 🖥 Interactive CLI

add @ChatUsername remove @ChatUsername list preview partial preview winner quit

### ⚙ Full Customization
All settings adjustable in `settings.json`.

---

# 🗂 Project Structure

telegram-777-monitor/ │ ├── interactive_monitor_777_with_buttons.py ├── settings.json ├── requirements.txt ├── .env.example ├── Dockerfile ├── docker-compose.yml ├── user_hits.json ├── LICENSE └── README.md

---

# ⚙ Environment Setup

Create `.env`:

API_ID=123456 API_HASH=your_api_hash_here STRING_SESSION= SESSION_NAME=monitor_session RESULTS_ACCOUNT=@YourResultsChannel

Generate string session:

python3 -m telethon.sessions

---

# ▶ Run on Linux / VPS

sudo apt update sudo apt install python3 python3-pip -y pip3 install -r requirements.txt python3 interactive_monitor_777_with_buttons.py

---

# 📱 Run on Termux (Android)

pkg update pkg install python git -y pip install --upgrade pip

git clone https://github.com/yourname/telegram-777-monitor cd telegram-777-monitor

pip install -r requirements.txt python interactive_monitor_777_with_buttons.py

---

# 🐳 Run via Docker

### Build:

docker build -t telegram-777-monitor .

### Run:

docker run --env-file .env telegram-777-monitor

---

# 🐙 Docker Compose

docker compose up -d

---

# ☁ Deploy on Render.com

1. Push project to GitHub  
2. Create Web Service  
3. Select Docker environment  
4. Add `.env` variables  
5. Deploy  

---

# 🪟 Run on Windows

pip install -r requirements.txt python interactive_monitor_777_with_buttons.py

Background:

Start-Job -ScriptBlock { python interactive_monitor_777_with_buttons.py }

---

# 🔥 Auto-Restart on Linux (systemd)

nano /etc/systemd/system/telegram-monitor.service



[Unit] Description=Telegram 777 Monitor After=network.target

[Service] WorkingDirectory=/root/telegram-777-monitor ExecStart=/usr/bin/python3 interactive_monitor_777_with_buttons.py Restart=always

[Install] WantedBy=multi-user.target

Enable service:

systemctl enable telegram-monitor systemctl start telegram-monitor

---

# 👑 Credits

Developed and maintained by @TON50B

If you find this useful, consider starring the repository.
