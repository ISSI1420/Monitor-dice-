<!-- PROJECT LOGO -->
<p align="center">
  <img src="https://img.icons8.com/fluency/96/dice.png" width="120"/>
</p>

<h1 align="center">🎰 Telegram 777 Dice Monitor Bot</h1>

<p align="center">
  Advanced Telethon-based monitoring bot that detects jackpot dice results (value 64), tracks user hits, and sends beautiful HTML notifications with dynamic inline buttons.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python%203.10-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Framework-Telethon-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge">
  <img src="https://img.shields.io/badge/Maintainer-@TON50B-purple?style=for-the-badge">
</p>

---

## 🚀 Overview

This bot monitors Telegram chats for **dice messages** and detects the jackpot value (**64**).  
It keeps track of user hits, stores them, and sends **fully dynamic notifications** including:

- 🧮 Hit counter per user  
- 🔗 Buttons linking to each dice message  
- 🏆 Automatic winner announcement  
- 🧰 Fully customizable templates  

It also includes an **interactive CLI** to manage chats, preview templates, and control behavior in real time.

---

## ✨ Features

### 🎯 Dice Detection   
Automatically detects dice messages and checks for the jackpot value (default: **64**).

### 📊 Hit Tracking  
Tracks hit counts per user and stores them persistently in `user_hits.json`.

### 📨 Dynamic Notifications  
Sends HTML-styled messages with clickable inline buttons:
- “Hit 1”
- “Hit 2”
- “Hit 3”
- ...

### 🖥 Interactive CLI
Control the entire bot while it is running:

add @ChatUsername remove @ChatUsername list preview partial preview winner quit

### ⚙ Fully Configurable
Edit everything in `settings.json`:
- Number of hits required to win  
- Dice target value  
- Templates  
- Result channel  

### 🐳 Production Deployment Support
- Termux
- Docker / Docker Compose
- Linux VPS
- Render.com
- Windows (CMD/PowerShell)

---



# ⚙ Configuration

Create a file named `.env`:

API_ID=123456 API_HASH=your_api_hash STRING_SESSION= SESSION_NAME=monitor_session RESULTS_ACCOUNT=@YourResultsChannel

Generate a String Session:

```bash
python3 -m telethon.sessions


---

▶ Run on Linux / VPS

sudo apt update
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
python3 interactive_monitor_777_with_buttons.py


---

📱 Run on Termux (Android)

pkg update
pkg install python git -y
pip install --upgrade pip

git clone https://github.com/yourname/telegram-777-monitor
cd telegram-777-monitor

pip install -r requirements.txt
python interactive_monitor_777_with_buttons.py


---

🐳 Run with Docker

Build:

docker build -t telegram-777-monitor .

Run:

docker run --env-file .env telegram-777-monitor


---

🐙 Docker Compose

docker compose up -d

Runs in background with auto-restart support.


---

☁ Deploy on Render.com (Docker)

1. Push repository to GitHub


2. Create a new Web Service


3. Select Docker environment


4. Add environment variables


5. Deploy instantly



Render will handle the Dockerfile automatically.


---

🪟 Windows (CMD / PowerShell)

pip install -r requirements.txt
python interactive_monitor_777_with_buttons.py

Run in background:

Start-Job -ScriptBlock { python interactive_monitor_777_with_buttons.py }


---

🧠 Target Chat Management (While Bot is Running)

add @ChatUsername
remove @ChatUsername
list
preview partial
preview winner


---

🔥 Auto-Restart (systemd)

nano /etc/systemd/system/telegram-monitor.service

Add:

[Unit]
Description=Telegram 777 Monitor
After=network.target

[Service]
WorkingDirectory=/root/telegram-777-monitor
ExecStart=/usr/bin/python3 interactive_monitor_777_with_buttons.py
Restart=always

[Install]
WantedBy=multi-user.target

Enable:

systemctl enable telegram-monitor
systemctl start telegram-monitor


---

👑 Credits

Developed and maintained by @TON50B


---

⭐ Support

If you like this project, consider giving it a GitHub Star ⭐
Your support helps the project grow!

</br>
