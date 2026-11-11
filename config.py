import os
from os import environ, getenv
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()


API_ID = int(environ.get("API_ID", 37562695))
API_HASH = environ.get("API_HASH", "684a41e9cb46f3987437dc9ae183138d")
BOT_TOKEN = environ.get("BOT_TOKEN", "8618914941:AAGkFvmZUrnrEj4Tz_AHj1NnBX5O50zgCVo")

STRING1 = environ.get("STRING1", "")
STRING2 = environ.get("STRING2", "")
STRING3 = environ.get("STRING3", "")
STRING4 = environ.get("STRING4", "")
STRING5 = environ.get("STRING5", "")

MONGO_DB_URI = getenv("MONGO_DB_URI", "")

OWNER_ID = int(environ.get("OWNER_ID", 8368077406))
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", -100123456789))
    
BUTTON_NAME = environ.get("BUTTON_NAME", "ᴠᴇɢᴀ")
BUTTON_URL = environ.get("BUTTON_URL", "https://t.me/TopVeGa")
YOUTUBE_COOKIES_PATH = environ.get("YOUTUBE_COOKIES_PATH", "/root/cookies")

BOT_USERNAME = environ.get("BOT_USERNAME", "")
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "vegaone")
DURATION_LIMIT = int(environ.get("DURATION_LIMIT", 900))
PLAYLIST_FETCH_LIMIT = int(environ.get("PLAYLIST_FETCH_LIMIT", 50))
    
PHOTO = environ.get("PHOTO", "https://telegra.ph/file/490756122766c26b39ab7.jpg")
GROUP = environ.get("GROUP", "https://t.me/vegaone")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/updatevega")
STREAM_IMG_URL = environ.get("STREAM_IMG_URL", "https://telegra.ph/file/490756122766c26b39ab7.jpg")
TELEGRAM_AUDIO_URL = environ.get("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/490756122766c26b39ab7.jpg")
TELEGRAM_VIDEO_URL = environ.get("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/490756122766c26b39ab7.jpg")
SOUNCLOUD_IMG_URL = environ.get("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/490756122766c26b39ab7.jpg")

LOGGER_ID = LOG_GROUP_ID if LOG_GROUP_ID != -100123456789 else OWNER_ID
LOGS = LOG_GROUP_ID
OWNER = environ.get("OWNER", "vegaone").split(",")
OWNER_NAME = environ.get("OWNER_NAME", "Vega")

SUDOERS = [int(x) for x in environ.get("SUDOERS", "8368077406").split(",")]

BANNED_USERS = set()
    
START_ENABLED = True
KEP_ENABLED = True
KEYBOARD_TIMEOUT = 300

MEDIA_CHANNELS = {
    "songs": "bsmaatt",
    "photos": "vnnkli", 
    "gifs": "GifWaTaN",
    "quotes": "LoreBots9",
    "headers": "flflfldld",
    "girls_photos": "vvyuol",
    "boys_photos": "vgbmm",
    "quran": "opuml",
    "sheikh": "ggcnjj",
    "stories": "yoipopl",
    "anime": "LoreBots7"
}

ASSISTANT_SESSIONS = [session for session in [STRING1, STRING2, STRING3, STRING4, STRING5] if session and session.strip()]
    
if not BOT_TOKEN:
    print("❌ خطأ: BOT_TOKEN غير موجود!")
    exit(1)
    
app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
    
__all__ = [
    'app', 'API_ID', 'API_HASH', 'BOT_TOKEN', 'OWNER_ID', 'LOG_GROUP_ID', 
    'OWNER', 'OWNER_NAME', 'LOGGER_ID', 'LOGS', 'BANNED_USERS', 
    'MONGO_DB_URI', 'PHOTO', 'GROUP', 'SUDOERS', 'STRING1', 'STRING2', 
    'STRING3', 'STRING4', 'STRING5', 'BOT_USERNAME', 'SUPPORT_CHAT',
    'DURATION_LIMIT', 'PLAYLIST_FETCH_LIMIT', 'STREAM_IMG_URL',
    'TELEGRAM_AUDIO_URL', 'TELEGRAM_VIDEO_URL', 'SOUNCLOUD_IMG_URL', 
    'ASSISTANT_SESSIONS', 'SUPPORT_CHANNEL',
    'BUTTON_NAME', 'BUTTON_URL', 'YOUTUBE_COOKIES_PATH',
    'START_ENABLED', 'KEP_ENABLED', 'KEYBOARD_TIMEOUT', 'MEDIA_CHANNELS'
]
    
PROTECTION_SETTINGS = {
    "auto_ban": True,
    "max_warns": 3,
    "mute_duration": 3600
} 