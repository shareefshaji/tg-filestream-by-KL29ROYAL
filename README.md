<h1 align="center">🎬 KL29 Royal Stream Bot</h1>

<p align="center">
  <b>A powerful Telegram File Streaming Bot — stream & generate direct links for any Telegram file</b>
</p>

<p align="center">
  <a href="https://github.com/shareefshaji/tg-filestream-by-KL29ROYAL/issues">🐛 Report Bug</a>
  ·
  <a href="https://github.com/shareefshaji/tg-filestream-by-KL29ROYAL/issues">✨ Request Feature</a>
</p>

<hr>

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Deploy on Railway](#-deploy-on-railway)
- [Run Locally / VPS](#-run-locally--vps)
- [Environment Variables](#-environment-variables)
- [Bot Commands](#-bot-commands)
- [FAQ](#-faq)
- [Credits](#-credits)

<hr>

## 📖 About

**KL29 Royal Stream Bot** is a Telegram bot that lets you stream and directly download any file shared on Telegram — without waiting for the full download to complete.

Built on top of [TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot) with a fully redesigned UI, improved messages, and better user experience.

<hr>

## ✨ Features

- 📁 Stream any Telegram file instantly via browser
- 🔗 Generate high-speed direct download links
- 🖥️ Watch videos & listen to audio online
- 👥 Multi-client support for faster streaming
- 🔒 Force join channel support
- 📢 Broadcast messages to all users
- 🚫 Ban / Unban user management
- 📊 Bot usage statistics
- 💾 MongoDB database integration
- 🌐 aiohttp web server built-in

<hr>

## 🚀 Deploy on Railway

The easiest way to host your bot 24/7 for free.

**1.** Go to [railway.app](https://railway.app) and sign up with GitHub

**2.** Click **New Project → Deploy from GitHub repo**
and select: `tg-filestream-by-KL29ROYAL`

**3.** Add your environment variables (see table below)

**4.** Set the start command:
```
python -m WebStreamer
```

**5.** After deploy → **Settings → Networking → Generate Domain**
Copy the URL and set it as your `FQDN` variable

<hr>

## 💻 Run Locally / VPS

```bash
# Clone the repo
git clone https://github.com/shareefshaji/tg-filestream-by-KL29ROYAL
cd tg-filestream-by-KL29ROYAL

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Create your .env file and fill variables
nano .env

# Run the bot
python3 -m WebStreamer
```

To stop: press `Ctrl + C`

**Run 24/7 on VPS with tmux:**
```bash
sudo apt install tmux -y
tmux new -s royalbot
python3 -m WebStreamer
# Detach with: Ctrl+B then D
```

<hr>

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=123456789:your_bot_token
OWNER_ID=123456789
BIN_CHANNEL=-100xxxxxxxxxx
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/db
FQDN=your-app.railway.app
HAS_SSL=True
NO_PORT=True
```

### Mandatory

| Variable | Description | How to Get |
|---|---|---|
| `API_ID` | Telegram API ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Your bot token | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | Your Telegram User ID | [@userinfobot](https://t.me/userinfobot) |
| `BIN_CHANNEL` | Channel ID for file storage (bot must be admin) | [@getidsbot](https://t.me/getidsbot) |
| `DATABASE_URL` | MongoDB connection URI | [MongoDB Atlas](https://www.mongodb.com/atlas) (free) |

### Optional

| Variable | Description | Default |
|---|---|---|
| `FQDN` | Your domain or server IP | `0.0.0.0` |
| `HAS_SSL` | Use HTTPS links (`True`/`False`) | `False` |
| `NO_PORT` | Hide port from links (`True`/`False`) | `False` |
| `PORT` | Web server port | `8080` |
| `WORKERS` | Concurrent bot workers | `6` |
| `SLEEP_THRESHOLD` | Flood wait threshold (seconds) | `60` |
| `PING_INTERVAL` | Keep-alive ping interval (seconds) | `1200` |
| `KEEP_ALIVE` | Ping server to prevent sleeping | `False` |
| `UPDATES_CHANNEL` | Your channel username (without @) | — |
| `FORCE_UPDATES_CHANNEL` | Force users to join channel | `False` |
| `SESSION_NAME` | MongoDB database name | `F2LxBot` |
| `ALLOWED_USERS` | Comma-separated allowed user IDs/usernames | (all users) |
| `IMAGE_FILEID` | Photo for /myfiles (file_id or URL) | Default image |
| `LINK_LIMIT` | Max links per free user | Unlimited |
| `TOS` | URL to Terms of Service text file | — |

### Multi-Client Setup

Add extra bot tokens to speed up streaming:

```env
MULTI_TOKEN1=111111111:first_bot_token
MULTI_TOKEN2=222222222:second_bot_token
MULTI_TOKEN3=333333333:third_bot_token
```

> ⚠️ All multi-client bots must be added as **admin** in `BIN_CHANNEL`

<hr>

## 🤖 Bot Commands

### User Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/help` | How to use the bot |
| `/about` | Bot info & version |
| `/myfiles` | Browse your generated links |
| `/info` | Your account details |
| `/tos` | View Terms of Service |

### Admin Commands (Owner only)

| Command | Description |
|---|---|
| `/status` | Bot stats (users, links, bans) |
| `/ban <UserID>` | Ban a user |
| `/unban <UserID>` | Unban a user |
| `/broadcast` | Broadcast a message (reply to a message) |
| `/getfile <id>` | Get a file by database ID |
| `/who` | See who sent a file (reply to file) |

<hr>

## ❓ FAQ

**How long are links valid?**
> Links stay valid as long as your bot is running and BIN_CHANNEL has not been deleted.

**Can multiple users use the bot at the same time?**
> Yes. Use multi-client setup with `MULTI_TOKEN1`, `MULTI_TOKEN2`, etc. for best performance.

**Is there a file size limit?**
> The limit follows Telegram's own limit — 2GB for bots.

**Why is my link not working after redeployment?**
> Update your `FQDN` variable to match your new domain URL.

<hr>

#
<hr>

<p align="center">Made with ❤️ for the Telegram community</p>
