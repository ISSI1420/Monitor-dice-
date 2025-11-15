# Copyright © @TON50B
import os
import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List

from telethon import TelegramClient, events, errors, Button
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', None)
STRING_SESSION = os.getenv('STRING_SESSION', None)
SESSION_NAME = os.getenv('SESSION_NAME', 'monitor_session')

if not API_HASH or API_ID == 0:
    raise SystemExit("Please set API_ID and API_HASH in .env")

if STRING_SESSION:
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
else:
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

SETTINGS_FILE = 'settings.json'
DEFAULT_SETTINGS = {
    "RESULTS_ACCOUNT": "@TON50B",
    "HITS_TO_WIN": 3,
    "DICE_TARGET_VALUE": 64,
    "PERSIST_FILE": "user_hits.json",
    "NOTIFICATION_TEMPLATES": {
        "partial_hit": "<b>🎰 Hit!</b>

<b>User:</b> {first_name}{username_part}
<b>Message link:</b>
<a href="{link}">Click to view</a>

<b>{remaining} hits remaining to win</b> 🏆",
        "winner": "<b>🎉 Winner! 🎉</b>

<b>User:</b> {first_name}{username_part}
<b>Completed {hits_needed} hits of {dice_value}!</b> 🏆

<b>Hit links:</b>
{links}

<b>Congratulations!</b> 🎰"
    }
}

def ensure_settings_file():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=2)
        logging.info("Created default settings.json — edit it to change templates/settings.")

def load_settings():
    ensure_settings_file()
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

settings = load_settings()
RESULTS_ACCOUNT = settings.get('RESULTS_ACCOUNT', DEFAULT_SETTINGS['RESULTS_ACCOUNT'])
HITS_TO_WIN = int(settings.get('HITS_TO_WIN', DEFAULT_SETTINGS['HITS_TO_WIN']))
DICE_TARGET_VALUE = int(settings.get('DICE_TARGET_VALUE', DEFAULT_SETTINGS['DICE_TARGET_VALUE']))
PERSIST_FILE = settings.get('PERSIST_FILE', DEFAULT_SETTINGS['PERSIST_FILE'])
TEMPLATES = settings.get('NOTIFICATION_TEMPLATES', DEFAULT_SETTINGS['NOTIFICATION_TEMPLATES'])

user_hits = {}
hits_lock = asyncio.Lock()
TARGET_CHATS: List[str] = []
targets_lock = asyncio.Lock()

def load_hits():
    global user_hits
    try:
        if os.path.exists(PERSIST_FILE):
            with open(PERSIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_hits = {int(k): v for k, v in data.items()}
            logging.info("Loaded persisted hits from %s", PERSIST_FILE)
        else:
            logging.info("No persist file found, starting fresh.")
    except Exception:
        logging.exception("Failed to load hits file")

def save_hits():
    try:
        to_save = {str(k): v for k, v in user_hits.items()}
        with open(PERSIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
    except Exception:
        logging.exception("Failed to save hits")

def escape_html(text: str) -> str:
    if text is None:
        return ''
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def parse_target_input(raw: str) -> List[str]:
    return [i.strip() for i in raw.split(',') if i.strip()]

async def add_targets(new_targets: List[str]):
    async with targets_lock:
        for t in new_targets:
            if t not in TARGET_CHATS:
                TARGET_CHATS.append(t)
        logging.info("Targets updated: %s", TARGET_CHATS)

async def remove_target(target: str):
    async with targets_lock:
        try:
            TARGET_CHATS.remove(target)
            logging.info("Removed target: %s", target)
        except ValueError:
            logging.warning("Target not in list: %s", target)

async def list_targets():
    async with targets_lock:
        if not TARGET_CHATS:
            print("No targets currently set.")
        else:
            print("Current targets:")
            for t in TARGET_CHATS:
                print(" -", t)

def is_chat_targeted(chat, target_list: List[str]) -> bool:
    chat_username = getattr(chat, 'username', '') or ''
    chat_title = getattr(chat, 'title', '') or ''
    chat_id = getattr(chat, 'id', None)
    for t in target_list:
        try:
            t_id = int(t)
            if chat_id == t_id:
                return True
        except Exception:
            pass
        norm_t = t.lstrip('@')
        if chat_username and chat_username.lower() == norm_t.lower():
            return True
        if chat_title and norm_t.lower() in chat_title.lower():
            return True
    return False

def build_hit_buttons(links_list: List[str]):
    buttons = []
    for i, item in enumerate(links_list, start=1):
        if isinstance(item, dict):
            url = item.get('link') or item.get('url') or ''
        else:
            try:
                url = str(item)
            except Exception:
                url = ''
        if not url:
            logging.debug("Skipping invalid link item at index %d: %r", i-1, item)
            continue
        buttons.append([Button.url(f"🎯 Hit {i}", url)])
    return buttons

async def safe_send_notification(template_key: str, context: dict, dest: str = RESULTS_ACCOUNT):
    tpl = TEMPLATES.get(template_key, "")
    if not tpl:
        logging.error("Template %s not found", template_key)
        return False

    username = context.get('username') or ''
    username_part = f" (@{escape_html(username)})" if username else ""
    raw_link = context.get('link', '')
    if isinstance(raw_link, dict):
        link = raw_link.get('link') or raw_link.get('url') or ''
    else:
        link = str(raw_link) if raw_link is not None else ''

    raw_links = context.get('links_list', [])
    normalized_links = []
    if raw_links:
        for it in raw_links:
            if isinstance(it, dict):
                u = it.get('link') or it.get('url') or ''
            else:
                u = str(it) if it is not None else ''
            if u:
                normalized_links.append(u)

    logging.debug("safe_send_notification normalized_links=%r link=%r", normalized_links, link)

    if normalized_links:
        links_formatted = "
".join([f"{i+1}. <a href="{escape_html(u)}">Link {i+1}</a>" for i, u in enumerate(normalized_links)])
    else:
        links_formatted = ""

    filled = tpl.format(
        first_name=escape_html(context.get('first_name', 'Unknown')),
        username=escape_html(username),
        username_part=username_part,
        username_display=(f"@{escape_html(username)}" if username else "—"),
        link=escape_html(link or "#"),
        remaining=context.get('remaining', 0),
        hits_needed=context.get('hits_needed', HITS_TO_WIN),
        dice_value=context.get('dice_value', DICE_TARGET_VALUE),
        links=links_formatted
    )

    if normalized_links:
        buttons = build_hit_buttons(normalized_links)
    elif link:
        buttons = [[Button.url("📩 View message", link)]]
    else:
        buttons = None

    max_tries = 3
    for attempt in range(1, max_tries + 1):
        try:
            await client.send_message(dest, filled, parse_mode='html', buttons=buttons, link_preview=False)
            return True
        except errors.FloodWaitError as fw:
            wait = min(fw.seconds, 60)
            logging.warning("FloodWait %s seconds — sleeping %s", fw.seconds, wait)
            await asyncio.sleep(wait)
        except Exception:
            logging.exception("Failed to send notification (attempt %d)", attempt)
            await asyncio.sleep(2 * attempt)
    logging.error("Giving up sending notification after %d attempts", max_tries)
    return False

@client.on(events.NewMessage)
async def monitor_messages(event):
    try:
        msg = event.message
        if not msg:
            return
        chat = await event.get_chat()
        sender = await event.get_sender()
        async with targets_lock:
            current_targets = list(TARGET_CHATS)
        if not current_targets:
            return
        if not is_chat_targeted(chat, current_targets):
            return
        dice = getattr(msg, 'dice', None)
        if not dice:
            return
        value = getattr(dice, 'value', None)
        if value is None:
            return
        if value == DICE_TARGET_VALUE:
            sender_id = getattr(sender, 'id', None)
            sender_username = getattr(sender, 'username', None)
            sender_first = getattr(sender, 'first_name', 'Unknown')
            msg_link = build_message_link(chat, msg.id)
            logging.info("Detected %s by %s (%s) in chat %s", value, sender_first, sender_username, getattr(chat, 'title', getattr(chat, 'username', 'unknown')))
            await process_777_hit(sender_id, sender_username, sender_first, msg_link)
    except Exception:
        logging.exception("Error in monitor_messages")

def build_message_link(chat, msg_id):
    try:
        if getattr(chat, 'username', None):
            return f"https://t.me/{chat.username}/{msg_id}"
        else:
            chat_id = str(getattr(chat, 'id', ''))
            if chat_id.startswith('-100'):
                base_id = chat_id.replace('-100', '', 1)
                return f"https://t.me/c/{base_id}/{msg_id}"
            else:
                return f"Message in group (ID: {chat_id})"
    except Exception:
        return "Link not available"

async def process_777_hit(sender_id, sender_username, sender_first, message_link):
    if sender_id is None:
        return
    async with hits_lock:
        data = user_hits.get(sender_id, {
            'username': sender_username,
            'first_name': sender_first,
            'hits': 0,
            'message_links': [],
            'last_hit_ts': None
        })
        data['hits'] += 1
        data['message_links'].append(message_link)
        data['username'] = sender_username
        data['first_name'] = sender_first
        data['last_hit_ts'] = datetime.now(timezone.utc).isoformat()
        user_hits[sender_id] = data
        save_hits()
        current_hits = data['hits']

    remaining = max(0, HITS_TO_WIN - current_hits)

    if current_hits < HITS_TO_WIN:
        ctx = {
            'first_name': sender_first,
            'username': sender_username,
            'link': message_link,
            'remaining': remaining,
            'dice_value': DICE_TARGET_VALUE,
            'links_list': data['message_links']
        }
        await safe_send_notification('partial_hit', ctx)
        logging.info("Notified partial hit for %s — %d/%d", sender_first, current_hits, HITS_TO_WIN)
    else:
        ctx = {
            'first_name': sender_first,
            'username': sender_username,
            'links_list': data['message_links'],
            'hits_needed': HITS_TO_WIN,
            'dice_value': DICE_TARGET_VALUE
        }
        await safe_send_notification('winner', ctx)
        logging.info("Announced winner: %s (%s)", sender_first, sender_username)
        async with hits_lock:
            user_hits[sender_id]['hits'] = 0
            user_hits[sender_id]['message_links'] = []
            user_hits[sender_id]['last_reset_ts'] = datetime.now(timezone.utc).isoformat()
            save_hits()

async def interactive_cli():
    loop = asyncio.get_event_loop()
    print("
Interactive CLI ready. Commands: add/remove/list/preview/quit")
    print(" preview <partial/winner>  -> show sample of template in terminal")
    while True:
        user_input = await loop.run_in_executor(None, input, "> ")
        if not user_input:
            continue
        parts = user_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == 'add':
            if not arg:
                print("Usage: add username_or_id[, another,...]")
                continue
            new = parse_target_input(arg)
            await add_targets(new)
            print("Added:", new)
        elif cmd == 'remove':
            if not arg:
                print("Usage: remove target")
                continue
            await remove_target(arg.strip())
            print("Removed (if existed):", arg.strip())
        elif cmd == 'list':
            await list_targets()
        elif cmd == 'preview':
            key = arg.strip().lower()
            if key in ('partial', 'partial_hit'):
                preview_template('partial_hit')
            elif key in ('winner', 'winning', 'winner_hit'):
                preview_template('winner')
            else:
                print("Usage: preview partial|winner")
        elif cmd == 'quit':
            print("Shutting down by user request...")
            await client.disconnect()
            os._exit(0)
        else:
            print("Unknown command. Use: add/remove/list/preview/quit")

def preview_template(template_key: str):
    tpl = TEMPLATES.get(template_key)
    if not tpl:
        print("Template not found:", template_key)
        return
    sample_ctx = {
        'first_name': 'SAMPLE_NAME',
        'username': 'SAMPLEUSER',
        'link': 'https://t.me/example/123',
        'remaining': 2,
        'hits_needed': HITS_TO_WIN,
        'dice_value': DICE_TARGET_VALUE,
        'links_list': ['https://t.me/example/111', 'https://t.me/example/222', 'https://t.me/example/333']
    }
    username = sample_ctx['username']
    username_part = f" (@{username})" if username else ""
    links_formatted = "
".join([f"{i+1}. <a href="{it}">Link {i+1}</a>" for i, it in enumerate(sample_ctx['links_list'])])
    filled = tpl.format(
        first_name=sample_ctx['first_name'],
        username=sample_ctx['username'],
        username_part=username_part,
        username_display=(f"@{username}" if username else "—"),
        link=sample_ctx['link'],
        remaining=sample_ctx['remaining'],
        hits_needed=sample_ctx['hits_needed'],
        dice_value=sample_ctx['dice_value'],
        links=links_formatted
    )
    print("
--- Template preview (raw HTML) ---
")
    print(filled)
    print("
--- End preview ---
")
    print("To change the template, edit", SETTINGS_FILE, "and restart the script (or use the preview command again).")

async def setup_bot_interactive():
    load_hits()
    if not TARGET_CHATS:
        raw = input("Enter target chat(s) (username or id or title substring). For multiple separate by commas:
> ").strip()
        if raw:
            initial = parse_target_input(raw)
            await add_targets(initial)
            logging.info("Initial targets set: %s", TARGET_CHATS)
        else:
            logging.info("No initial targets set. Use CLI commands to add targets later.")
    await client.start()
    logging.info("=" * 50)
    logging.info("🔧 Monitoring target dice value %s with dynamic buttons", DICE_TARGET_VALUE)
    logging.info("📨 Notifications to: %s", RESULTS_ACCOUNT)
    logging.info("🚀 Monitoring started...")
    logging.info("=" * 50)
    asyncio.create_task(interactive_cli())

async def main():
    await setup_bot_interactive()
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Shutting down (KeyboardInterrupt)")
