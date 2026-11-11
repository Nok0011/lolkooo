import asyncio
from typing import Dict, List, Union, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import UserNotParticipant, ChannelInvalid, InviteHashExpired, InviteRequestSent, UserAlreadyParticipant, ChatAdminRequired
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, ASSISTANT_SESSIONS, MONGO_DB_URI, OWNER_ID, LOG_GROUP_ID, GROUP

try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.Harmony
    persistent_db = _mongo_async_["KIM"]["Fox"]
except Exception as e:
    print(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
    exit()


authdb = mongodb.adminauth
authuserdb = mongodb.authuser
autoenddb = mongodb.autoend
assdb = mongodb.assistants
blacklist_chatdb = mongodb.blacklistChat
blockeddb = mongodb.blockedusers
chatsdb = mongodb.chats
channeldb = mongodb.cplaymode
countdb = mongodb.upcount
gbansdb = mongodb.gban
langdb = mongodb.language
onoffdb = mongodb.onoffper
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
skipdb = mongodb.skipmode
sudoersdb = mongodb.sudoers
usersdb = mongodb.tgusersdb
chmustdb = mongodb.chmust



abraag_collection = persistent_db.abraag
mention_all_collection = persistent_db.mention_all
hms_collection = persistent_db.hms_messages
azan_collection = persistent_db.azan
azan_playback_collection = persistent_db.azan_playback
cleanup_collection = persistent_db.cleanup_sessions
youtube_settings_collection = persistent_db.youtube_settings
command_settings_collection = persistent_db.command_settings
keyboard_settings_collection = persistent_db.keyboard_settings
user_sessions_collection = persistent_db.user_sessions
user_keyboards_collection = persistent_db.user_keyboards
restricted_users_collection = persistent_db.restricted_users
muted_users_collection = persistent_db.muted_users
banned_users_collection = persistent_db.banned_users
queue_collection = persistent_db.queues
current_playing_collection = persistent_db.current_playing
active_chats_collection = persistent_db.active_chats


ranks_moteerr_collection = persistent_db.ranks_moteerr
ranks_malkeen_collection = persistent_db.ranks_malkeen
ranks_mutaw_collection = persistent_db.ranks_mutaw
ranks_admann_collection = persistent_db.ranks_admann



active = []
activevideo = []
assistantdict = {}
autoend = {}
count = {}
channelconnect = {}
langm = {}
loop = {}
maintenance = []
nonadmin = {}
pause = {}
playmode = {}
playtype = {}
skipmode = {}
mute = {}
current_playing = {}
queue = {}

userbot = None
call = None

()

async def is_abraag_enabled(chat_id: int) -> bool:
    doc = await abraag_collection.find_one({"chat_id": chat_id})
    return doc is None 

async def disable_abraag(chat_id: int):
    await abraag_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"disabled": True, "updated_at": datetime.now()}},
        upsert=True
    )

async def enable_abraag(chat_id: int):
    await abraag_collection.delete_one({"chat_id": chat_id})

async def is_mention_all_enabled(chat_id: int) -> bool:
    doc = await mention_all_collection.find_one({"chat_id": chat_id})
    return doc is None  

async def disable_mention_all(chat_id: int):
    await mention_all_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"disabled": True, "updated_at": datetime.now()}},
        upsert=True
    )

async def enable_mention_all(chat_id: int):
    await mention_all_collection.delete_one({"chat_id": chat_id})

async def get_abraag_status(chat_id: int) -> bool:
    return await is_abraag_enabled(chat_id)

async def get_mention_all_status(chat_id: int) -> bool:
    return await is_mention_all_enabled(chat_id)


async def save_hms_message(target_user_id: int, hms_id: int, data: dict):
    await hms_collection.update_one(
        {"target_user_id": target_user_id, "hms_id": hms_id},
        {"$set": {**data, "saved_at": datetime.now()}},
        upsert=True
    )

async def get_hms_message(target_user_id: int, hms_id: int) -> dict:
    doc = await hms_collection.find_one({"target_user_id": target_user_id, "hms_id": hms_id})
    if doc:
        doc.pop('_id', None)
        doc.pop('saved_at', None)
    return doc

async def delete_hms_message(target_user_id: int, hms_id: int):
    await hms_collection.delete_one({"target_user_id": target_user_id, "hms_id": hms_id})


async def is_azan_enabled(chat_id: int) -> bool:
    doc = await azan_collection.find_one({"chat_id": chat_id})
    return doc is not None

async def enable_azan(chat_id: int):
    await azan_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": True, "updated_at": datetime.now()}},
        upsert=True
    )

async def disable_azan(chat_id: int):
    await azan_collection.delete_one({"chat_id": chat_id})

async def get_azan_chats() -> list:
    chats = []
    async for doc in azan_collection.find({}):
        chats.append(doc["chat_id"])
    return chats


async def save_playback_state(chat_id: int, state: dict):
    await azan_playback_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {**state, "saved_at": datetime.now()}},
        upsert=True
    )

async def get_playback_state(chat_id: int) -> dict:
    doc = await azan_playback_collection.find_one({"chat_id": chat_id})
    if doc:
        doc.pop('_id', None)
        doc.pop('saved_at', None)
    return doc

async def clear_playback_state(chat_id: int):
    await azan_playback_collection.delete_one({"chat_id": chat_id})



async def add_cleanup_session(chat_id: int, user_id: int):
    await cleanup_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "user_id": user_id,
            "start_time": datetime.now(),
            "status": "active"
        }},
        upsert=True
    )

async def remove_cleanup_session(chat_id: int):
    await cleanup_collection.delete_one({"chat_id": chat_id})

async def get_cleanup_session(chat_id: int) -> dict:
    doc = await cleanup_collection.find_one({"chat_id": chat_id})
    if doc:
        doc.pop('_id', None)
    return doc

async def is_cleanup_active(chat_id: int) -> bool:
    doc = await cleanup_collection.find_one({"chat_id": chat_id})
    return doc is not None



async def is_youtube_disabled(chat_id: int) -> bool:
    global_doc = await youtube_settings_collection.find_one({"type": "global"})
    local_doc = await youtube_settings_collection.find_one({"type": "local_disabled", "chats": chat_id})
    
    return (global_doc is not None and global_doc.get("disabled", False)) or local_doc is not None

async def disable_youtube_global():
    await youtube_settings_collection.update_one(
        {"type": "global"},
        {"$set": {"disabled": True, "updated_at": datetime.now()}},
        upsert=True
    )

async def enable_youtube_global():
    await youtube_settings_collection.update_one(
        {"type": "global"},
        {"$set": {"disabled": False, "updated_at": datetime.now()}},
        upsert=True
    )

async def disable_youtube_local(chat_id: int):
    await youtube_settings_collection.update_one(
        {"type": "local_disabled"},
        {"$addToSet": {"chats": chat_id}},
        upsert=True
    )

async def enable_youtube_local(chat_id: int):
    await youtube_settings_collection.update_one(
        {"type": "local_disabled"},
        {"$pull": {"chats": chat_id}},
        upsert=True
    )


async def is_command_disabled(command: str, chat_id: int) -> bool:
    doc = await command_settings_collection.find_one({"command": command, "chats": chat_id})
    return doc is not None

async def disable_command(command: str, chat_id: int):
    await command_settings_collection.update_one(
        {"command": command},
        {"$addToSet": {"chats": chat_id}},
        upsert=True
    )

async def enable_command(command: str, chat_id: int):
    await command_settings_collection.update_one(
        {"command": command},
        {"$pull": {"chats": chat_id}},
        upsert=True
    )


async def is_keyboard_command_disabled(chat_id: int, command: str) -> bool:
    doc = await keyboard_settings_collection.find_one({"chat_id": chat_id, "disabled_commands": command})
    return doc is not None

async def disable_keyboard_command(chat_id: int, command: str):
    await keyboard_settings_collection.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"disabled_commands": command}},
        upsert=True
    )

async def enable_keyboard_command(chat_id: int, command: str):
    await keyboard_settings_collection.update_one(
        {"chat_id": chat_id},
        {"$pull": {"disabled_commands": command}},
        upsert=True
    )

async def get_user_keyboard(user_id: int) -> dict:
    doc = await user_keyboards_collection.find_one({"user_id": user_id})
    return doc.get("settings", {}) if doc else {}

async def set_user_keyboard(user_id: int, settings: dict):
    await user_keyboards_collection.update_one(
        {"user_id": user_id},
        {"$set": {"settings": settings, "updated_at": datetime.now()}},
        upsert=True
    )

async def save_user_session(user_id: int, session_data: dict):
    await user_sessions_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            **session_data,
            "last_activity": datetime.now()
        }},
        upsert=True
    )

async def get_user_session(user_id: int) -> dict:
    doc = await user_sessions_collection.find_one({"user_id": user_id})
    if doc:
        doc.pop('_id', None)
    return doc

async def cleanup_expired_sessions():
    cutoff_time = datetime.now().timestamp() - 3600  # ساعة واحدة
    await user_sessions_collection.delete_many({
        "last_activity": {"$lt": cutoff_time}
    })



async def add_restricted_user(chat_id: int, user_id: int):
    await restricted_users_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"timestamp": datetime.now(), "type": "restricted"}},
        upsert=True
    )

async def remove_restricted_user(chat_id: int, user_id: int):
    await restricted_users_collection.delete_one({"chat_id": chat_id, "user_id": user_id})

async def get_restricted_users(chat_id: int) -> list:
    users = []
    async for user in restricted_users_collection.find({"chat_id": chat_id, "type": "restricted"}):
        users.append(user["user_id"])
    return users

async def is_user_restricted(chat_id: int, user_id: int) -> bool:
    user = await restricted_users_collection.find_one({"chat_id": chat_id, "user_id": user_id, "type": "restricted"})
    return user is not None

async def clear_restricted_users(chat_id: int):
    await restricted_users_collection.delete_many({"chat_id": chat_id, "type": "restricted"})

async def add_muted_user(chat_id: int, user_id: int):
    await muted_users_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"timestamp": datetime.now(), "type": "muted"}},
        upsert=True
    )

async def remove_muted_user(chat_id: int, user_id: int):
    await muted_users_collection.delete_one({"chat_id": chat_id, "user_id": user_id})

async def get_muted_users(chat_id: int) -> list:
    users = []
    async for user in muted_users_collection.find({"chat_id": chat_id, "type": "muted"}):
        users.append(user["user_id"])
    return users

async def is_user_muted(chat_id: int, user_id: int) -> bool:
    user = await muted_users_collection.find_one({"chat_id": chat_id, "user_id": user_id, "type": "muted"})
    return user is not None

async def clear_muted_users(chat_id: int):
    await muted_users_collection.delete_many({"chat_id": chat_id, "type": "muted"})

async def add_banned_user(chat_id: int, user_id: int):
    await banned_users_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"timestamp": datetime.now(), "type": "banned"}},
        upsert=True
    )

async def remove_banned_user(chat_id: int, user_id: int):
    await banned_users_collection.delete_one({"chat_id": chat_id, "user_id": user_id})

async def get_banned_users(chat_id: int) -> list:
    users = []
    async for user in banned_users_collection.find({"chat_id": chat_id, "type": "banned"}):
        users.append(user["user_id"])
    return users

async def is_user_banned(chat_id: int, user_id: int) -> bool:
    user = await banned_users_collection.find_one({"chat_id": chat_id, "user_id": user_id, "type": "banned"})
    return user is not None

async def clear_banned_users(chat_id: int):
    await banned_users_collection.delete_many({"chat_id": chat_id, "type": "banned"})



async def get_current_playing(chat_id: int) -> Dict:
    
    if chat_id in current_playing:
        return current_playing[chat_id]
    

    doc = await current_playing_collection.find_one({"chat_id": chat_id})
    if doc:
        doc.pop('_id', None)
        doc.pop('saved_at', None)
      
        current_playing[chat_id] = doc
        return doc
    return None

async def set_current_playing(chat_id: int, data: Dict):
    current_playing[chat_id] = data
    await current_playing_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {**data, "saved_at": datetime.now()}},
        upsert=True
    )

async def remove_current_playing(chat_id: int):
    if chat_id in current_playing:
        del current_playing[chat_id]
    await current_playing_collection.delete_one({"chat_id": chat_id})

async def get_queue(chat_id: int) -> List[Dict]:
    if chat_id in queue:
        return queue[chat_id]
    
    doc = await queue_collection.find_one({"chat_id": chat_id})
    if doc:
        queue_list = doc.get("queue", [])
        queue[chat_id] = queue_list
        return queue_list
    return []

async def add_to_queue(chat_id: int, file_path: str, yturl: str, title: str, duration: str, videoid: str, vid: bool, user_id: int, position: int = None, user_info: str = None) -> int:
    queue_item = {
        "file_path": file_path,
        "yturl": yturl,
        "title": title,
        "duration": duration,
        "videoid": videoid,
        "vid": vid,
        "user_id": user_id,
        "user_info": user_info,  
        "added_at": datetime.now()
    }
    

    current_queue = await get_queue(chat_id)
    
    if position is not None and 0 <= position < len(current_queue):
        current_queue.insert(position, queue_item)
    else:
        current_queue.append(queue_item)
    

    queue[chat_id] = current_queue
    

    await queue_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"queue": current_queue, "updated_at": datetime.now()}},
        upsert=True
    )
    
    return len(current_queue)

async def remove_from_queue(chat_id: int, index: int):
    current_queue = await get_queue(chat_id)
    if 0 <= index < len(current_queue):
        current_queue.pop(index)
        
        queue[chat_id] = current_queue
        
     
        await queue_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"queue": current_queue, "updated_at": datetime.now()}},
            upsert=True
        )
        return True
    return False

async def clear_queue(chat_id: int):
    # مسح من الذاكرة المؤقتة
    if chat_id in queue:
        del queue[chat_id]
    
    # مسح من قاعدة البيانات
    await queue_collection.delete_one({"chat_id": chat_id})

# =================================
# دوال الحساب المساعد
# =================================

async def get_userbot(bot_username=None):
    global userbot, call    
    if userbot is not None:
        return userbot    
    if not ASSISTANT_SESSIONS or not ASSISTANT_SESSIONS[0]:
        return None   
    try:
        userbot = Client(
            name="assistant",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=ASSISTANT_SESSIONS[0],
            in_memory=True
        )        
        await userbot.start()
        call = PyTgCalls(userbot)
        await call.start()
        return userbot       
    except Exception:
        return None

async def get_call(bot_username=None):
    global call
    return call

async def join_assistant_to_chat(client, chat_id, bot_username):
    try:
        userbot = await get_userbot(bot_username)
        if not userbot:
            return False        
        try:
            chat = await client.get_chat(chat_id)
        except Exception:
            return False        
        try:
            member = await userbot.get_chat_member(chat_id, (await userbot.get_me()).id)
            if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                return True
        except (UserNotParticipant, ChannelInvalid):
            pass
        except Exception:
            pass        
        if chat.username:
            try:
                await userbot.join_chat(chat.username)
                return True
            except Exception:
                pass        
        try:
            await userbot.join_chat(chat_id)
            return True
        except (InviteHashExpired, InviteRequestSent, UserAlreadyParticipant):
            return True
        except Exception:
            pass        
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
            if invite_link:
                await userbot.join_chat(invite_link)
                return True
        except ChatAdminRequired:
            try:
                chat_info = await client.get_chat(chat_id)
                if chat_info.invite_link:
                    await userbot.join_chat(chat_info.invite_link)
                    return True
            except Exception:
                pass
        except Exception:
            pass        
        return False                    
    except Exception:
        return False

async def ensure_assistant_joined(client, chat_id, bot_username):
    max_retries = 2
    for attempt in range(max_retries):
        try:
            success = await join_assistant_to_chat(client, chat_id, bot_username)
            if success:
                return True
            elif attempt < max_retries - 1:
                await asyncio.sleep((attempt + 1) * 2)
        except Exception:
            if attempt < max_retries - 1:
                await asyncio.sleep(2)    
    return False

async def send_start_to_bot(bot_username):
    try:
        userbot = await get_userbot(bot_username)
        if not userbot:
            return False        
        try:
            bot_info = await userbot.get_users(bot_username)
            if not bot_info or not bot_info.is_bot:
                return False
        except Exception:
            return False        
        await userbot.send_message(bot_username, "/start")
        return True        
    except Exception:
        return False

# =================================
# دوال المساعدين
# =================================

async def get_assistant_number(chat_id: int) -> str:
    return assistantdict.get(chat_id)

async def get_client(assistant: int):
    return userbot

async def set_assistant_new(chat_id, number):
    number = int(number)
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )

async def set_assistant(chat_id):
    ran_assistant = 1
    assistantdict[chat_id] = ran_assistant
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    userbot_client = await get_client(ran_assistant)
    return userbot_client

async def get_assistant(chat_id: int):
    assistant = assistantdict.get(chat_id)    
    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            userbot_client = await set_assistant(chat_id)
            return userbot_client
        else:
            got_assis = dbassistant["assistant"]
            assistantdict[chat_id] = got_assis
            userbot_client = await get_client(got_assis)
            return userbot_client
    else:
        userbot_client = await get_client(assistant)
        return userbot_client

async def set_calls_assistant(chat_id):
    ran_assistant = 1
    assistantdict[chat_id] = ran_assistant
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant

async def group_assistant(self, chat_id: int) -> int:
    assistant = assistantdict.get(chat_id)    
    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = dbassistant["assistant"]
            assistantdict[chat_id] = assis
    else:
        assis = assistant   
    return userbot

# =================================
# دوال إعدادات التشغيل
# =================================

async def is_skipmode(chat_id: int) -> bool:
    mode = skipmode.get(chat_id)
    if not mode:
        user = await skipdb.find_one({"chat_id": chat_id})
        if not user:
            skipmode[chat_id] = True
            return True
        skipmode[chat_id] = False
        return False
    return mode

async def skip_on(chat_id: int):
    skipmode[chat_id] = True
    user = await skipdb.find_one({"chat_id": chat_id})
    if user:
        return await skipdb.delete_one({"chat_id": chat_id})

async def skip_off(chat_id: int):
    skipmode[chat_id] = False
    user = await skipdb.find_one({"chat_id": chat_id})
    if not user:
        return await skipdb.insert_one({"chat_id": chat_id})

async def get_upvote_count(chat_id: int) -> int:
    mode = count.get(chat_id)
    if not mode:
        mode = await countdb.find_one({"chat_id": chat_id})
        if not mode:
            return 5
        count[chat_id] = mode["mode"]
        return mode["mode"]
    return mode

async def set_upvotes(chat_id: int, mode: int):
    count[chat_id] = mode
    await countdb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def is_autoend() -> bool:
    chat_id = 1234
    user = await autoenddb.find_one({"chat_id": chat_id})
    return user is not None

async def autoend_on():
    chat_id = 1234
    await autoenddb.insert_one({"chat_id": chat_id})

async def autoend_off():
    chat_id = 1234
    await autoenddb.delete_one({"chat_id": chat_id})

async def get_loop(chat_id: int) -> int:
    return loop.get(chat_id, 0)

async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode

async def get_cmode(chat_id: int) -> int:
    mode = channelconnect.get(chat_id)
    if not mode:
        mode = await channeldb.find_one({"chat_id": chat_id})
        if not mode:
            return None
        channelconnect[chat_id] = mode["mode"]
        return mode["mode"]
    return mode

async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if not mode:
        mode = await playtypedb.find_one({"chat_id": chat_id})
        if not mode:
            playtype[chat_id] = "Everyone"
            return "Everyone"
        playtype[chat_id] = mode["mode"]
        return mode["mode"]
    return mode

async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if not mode:
        mode = await playmodedb.find_one({"chat_id": chat_id})
        if not mode:
            playmode[chat_id] = "Direct"
            return "Direct"
        playmode[chat_id] = mode["mode"]
        return mode["mode"]
    return mode

async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if not mode:
        lang = await langdb.find_one({"chat_id": chat_id})
        if not lang:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    return mode

async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)

# =================================
# دوال التحكم في التشغيل
# =================================

async def is_music_playing(chat_id: int) -> bool:
    return pause.get(chat_id, True)

async def music_on(chat_id: int):
    pause[chat_id] = True

async def music_off(chat_id: int):
    pause[chat_id] = False

async def is_stream_paused(chat_id: int) -> bool:
    return not pause.get(chat_id, True)

async def is_stream_playing(chat_id: int) -> bool:
    current = await get_current_playing(chat_id)
    return current is not None and current.get('file_path') is not None

async def is_muted(chat_id: int) -> bool:
    return mute.get(chat_id, False)


# أضف في database.py بعد دوال المساعدين

# =================================
# نظام إدارة المساعد في الكول (جديد)
# =================================

# متغيرات تتبع حالة المساعد في الكول
assistant_in_call = {}

async def keep_assistant_in_call(chat_id: int):
    """الحفاظ على المساعد في الكول"""
    global assistant_in_call
    assistant_in_call[chat_id] = True

async def release_assistant_from_call(chat_id: int):
    """تحرير المساعد من الكول"""
    global assistant_in_call
    assistant_in_call[chat_id] = False

async def is_assistant_in_call(chat_id: int) -> bool:
    """التحقق إذا كان المساعد في الكول"""
    return assistant_in_call.get(chat_id, False)

async def manage_assistant_presence(chat_id: int, should_stay: bool = None):
    """إدارة وجود المساعد في الكول"""
    if should_stay is not None:
        if should_stay:
            await keep_assistant_in_call(chat_id)
        else:
            await release_assistant_from_call(chat_id)
    return await is_assistant_in_call(chat_id)
    
# =================================
# دوال الدردشات النشطة
# =================================

async def get_active_chats() -> list:
    return active

async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active

async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

async def get_active_video_chats() -> list:
    return activevideo

async def is_active_video_chat(chat_id: int) -> bool:
    return chat_id in activevideo

async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)

async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)


async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    return user is not None

async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if not mode:
        user = await authdb.find_one({"chat_id": chat_id})
        if not user:
            nonadmin[chat_id] = False
            return False
        nonadmin[chat_id] = True
        return True
    return mode

async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    is_admin = await check_nonadmin_chat(chat_id)
    if not is_admin:
        return await authdb.insert_one({"chat_id": chat_id})

async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return await authdb.delete_one({"chat_id": chat_id})


async def is_on_off(on_off: int) -> bool:
    onoff = await onoffdb.find_one({"on_off": on_off})
    return onoff is not None

async def add_on(on_off: int):
    is_on = await is_on_off(on_off)
    if not is_on:
        return await onoffdb.insert_one({"on_off": on_off})

async def add_off(on_off: int):
    is_off = await is_on_off(on_off)
    if is_off:
        return await onoffdb.delete_one({"on_off": on_off})

async def is_play_log_enabled() -> bool:
    return await is_on_off(2)

async def enable_play_log():
    is_enabled = await is_play_log_enabled()
    if not is_enabled:
        return await add_on(2)

async def disable_play_log():
    is_enabled = await is_play_log_enabled()
    if is_enabled:
        return await add_off(2)

async def is_maintenance():
    if not maintenance:
        get = await onoffdb.find_one({"on_off": 1})
        if not get:
            maintenance.clear()
            maintenance.append(2)
            return True
        else:
            maintenance.clear()
            maintenance.append(1)
            return False
    else:
        return 1 not in maintenance

async def maintenance_off():
    maintenance.clear()
    maintenance.append(2)
    is_off = await is_on_off(1)
    if is_off:
        return await onoffdb.delete_one({"on_off": 1})

async def maintenance_on():
    maintenance.clear()
    maintenance.append(1)
    is_on = await is_on_off(1)
    if not is_on:
        return await onoffdb.insert_one({"on_off": 1})


async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return user is not None

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if not is_served:
        return await usersdb.insert_one({"user_id": user_id})

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return chat is not None

async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return await chatsdb.insert_one({"chat_id": chat_id})

async def remove_served_chat(chat_id: int):
    if await is_served_chat(chat_id):
        await chatsdb.delete_one({"chat_id": chat_id})


async def blacklisted_chats() -> list:
    chats_list = []
    async for chat in blacklist_chatdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list

async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False

async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False



async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]

async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = await _get_authusers(chat_id)
    return list(_notes.keys())

async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    _notes = await _get_authusers(chat_id)
    return _notes.get(name, False)

async def save_authuser(chat_id: int, name: str, note: dict):
    _notes = await _get_authusers(chat_id)
    _notes[name] = note
    await authuserdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )

async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False



async def get_gbanned() -> list:
    results = []
    async for user in gbansdb.find({"user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results

async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    return user is not None

async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return await gbansdb.insert_one({"user_id": user_id})

async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return await gbansdb.delete_one({"user_id": user_id})



async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]

async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    if user_id not in sudoers:
        sudoers.append(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
    return True

async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    if user_id in sudoers:
        sudoers.remove(user_id)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
    return True


async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({"user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results

async def get_banned_count() -> int:
    users = blockeddb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)

async def is_banned_user(user_id: int) -> bool:
    user = await blockeddb.find_one({"user_id": user_id})
    return user is not None

async def add_banned_user(user_id: int):
    is_banned = await is_banned_user(user_id)
    if not is_banned:
        return await blockeddb.insert_one({"user_id": user_id})

async def remove_banned_user(user_id: int):
    is_banned = await is_banned_user(user_id)
    if is_banned:
        return await blockeddb.delete_one({"user_id": user_id})



async def get_group(bot_username):
    try:
        return GROUP
    except:
        return None

async def get_channel(bot_username):
    try:
        return LOG_GROUP_ID
    except:
        return None


async def cleanup_chat_data(chat_id):
    await remove_active_chat(chat_id)
    await remove_active_video_chat(chat_id)
    await remove_current_playing(chat_id)
    await clear_queue(chat_id)    
    if chat_id in current_playing:
        del current_playing[chat_id]
    if chat_id in queue:
        del queue[chat_id]

async def get_remaining_queue_count(chat_id):
    queue_list = await get_queue(chat_id)
    return len(queue_list) if queue_list else 0



rankdb = mongodb.ranks

moteerr = {}  
malkeen = {}  
mutaw = {}    
admann = {}   

async def load_ranks_from_db():
    global moteerr, malkeen, mutaw, admann    
    try:
        ranks_data = await rankdb.find_one({"type": "group_ranks"})
        if ranks_data:
            # تحويل string keys إلى integers
            moteerr = {int(k): v for k, v in ranks_data.get("moteerr", {}).items()}
            malkeen = {int(k): v for k, v in ranks_data.get("malkeen", {}).items()}
            mutaw = {int(k): v for k, v in ranks_data.get("mutaw", {}).items()}
            admann = {int(k): v for k, v in ranks_data.get("admann", {}).items()}
            print(f"✅ تم تحميل الرتب: {len(moteerr)} مدير, {len(malkeen)} مالك, {len(mutaw)} مطور, {len(admann)} ادمن")
        else:
            print("ℹ️ لا توجد بيانات رتب محفوظة")
    except Exception as e:
        print(f"❌ خطأ في تحميل الرتب: {e}")

async def save_ranks_to_db():
    try:
        await rankdb.update_one(
            {"type": "group_ranks"},
            {"$set": {
                "moteerr": {str(k): v for k, v in moteerr.items()},
                "malkeen": {str(k): v for k, v in malkeen.items()},
                "mutaw": {str(k): v for k, v in mutaw.items()},
                "admann": {str(k): v for k, v in admann.items()},
                "last_updated": datetime.now()
            }},
            upsert=True
        )
        print(f"💾 تم حفظ الرتب: {len(moteerr)} مدير, {len(malkeen)} مالك, {len(mutaw)} مطور, {len(admann)} ادمن")
    except Exception as e:
        print(f"❌ خطأ في حفظ الرتب: {e}")

def is_owner(_, __, message):
    if not message or not message.from_user:
        return False
    return message.from_user.id in [OWNER_ID, 6753126490, 6760053475]
    
async def is_admin(message):
    if not message or not message.from_user:
        return False        
    user = message.from_user
    if user.id in [OWNER_ID, 6753126490, 6760053475]:
        return True        
    try:
        member = await message.chat.get_member(user.id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except:
        return False    
    
def is_moteerr(user_id):
    return user_id in moteerr and moteerr[user_id] > 0

def is_malkeen(user_id):
    return user_id in malkeen and malkeen[user_id] > 0

def is_mutaw(user_id):
    return user_id in mutaw and mutaw[user_id] > 0

def is_admann(user_id):
    return user_id in admann and admann[user_id] > 0

async def add_moteerr(user_id: int):
    moteerr[user_id] = 1
    await save_ranks_to_db()

async def remove_moteerr(user_id: int):
    if user_id in moteerr:
        del moteerr[user_id]
        await save_ranks_to_db()

async def add_malkeen(user_id: int):
    malkeen[user_id] = 1
    await save_ranks_to_db()

async def remove_malkeen(user_id: int):
    if user_id in malkeen:
        del malkeen[user_id]
        await save_ranks_to_db()

async def add_mutaw(user_id: int):
    mutaw[user_id] = 1
    await save_ranks_to_db()

async def remove_mutaw(user_id: int):
    if user_id in mutaw:
        del mutaw[user_id]
        await save_ranks_to_db()

async def add_admann(user_id: int):
    admann[user_id] = 1
    await save_ranks_to_db()

async def remove_admann(user_id: int):
    if user_id in admann:
        del admann[user_id]
        await save_ranks_to_db()

async def get_moteerr_list():
    return [user_id for user_id, rank in moteerr.items() if rank > 0]

async def get_malkeen_list():
    return [user_id for user_id, rank in malkeen.items() if rank > 0]

async def get_mutaw_list():
    return [user_id for user_id, rank in mutaw.items() if rank > 0]

async def get_admann_list():
    return [user_id for user_id, rank in admann.items() if rank > 0]

async def clear_all_ranks():
    global moteerr, malkeen, mutaw, admann
    moteerr.clear()
    malkeen.clear()
    mutaw.clear()
    admann.clear()
    await save_ranks_to_db()
    


async def load_all_persistent_data():
    try:
        await load_ranks_from_db()
    except Exception as e:
        print(f"❌ خطأ في تحميل البيانات المحفوظة: {e}")


_initialized = False

async def initialize_database():
    global _initialized
    if not _initialized:
        await load_all_persistent_data()
        _initialized = True
        print("✅ تم تحميل قاعدة البيانات بنجاح مع التخزين الدائم")

def get_initialize_task():
    return initialize_database()