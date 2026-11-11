import asyncio
import importlib
import sys
import os
import glob
import traceback
from datetime import datetime
import pytz
from pyromod import listen
from config import app, API_ID, API_HASH, BOT_TOKEN, ASSISTANT_SESSIONS, STRING1, STRING2, STRING3, STRING4, STRING5, BOT_USERNAME, LOGGER_ID
from database import get_userbot, get_call, initialize_database, send_start_to_bot
from config import BANNED_USERS, OWNER_ID, SUDOERS, OWNER
from pyrogram import Client, idle
from pyrogram.types import BotCommand, BotCommandScopeAllChatAdministrators, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, InlineKeyboardMarkup, InlineKeyboardButton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

assistants = []
assistantids = []

GROUPS_TO_JOIN = ["vipvega", "vegaone", "CEOVEGA", "Python2015"]

async def load_plugins():
    plugin_dir = "plugin"
    loaded_plugins = []
    failed_plugins = []  
    if not os.path.exists(plugin_dir):
        print(f"❌ مجلد الإضافات {plugin_dir} غير موجود!")
        return loaded_plugins, failed_plugins    
    plugin_files = glob.glob(os.path.join(plugin_dir, "*.py"))
    plugin_files = [f for f in plugin_files if not f.endswith("__init__.py")]   
    if not plugin_files:
        return loaded_plugins, failed_plugins
    for plugin_file in plugin_files:
        plugin_name = os.path.basename(plugin_file)[:-3]
        try:
            plugin_dir_abs = os.path.abspath(plugin_dir)
            if plugin_dir_abs not in sys.path:
                sys.path.insert(0, plugin_dir_abs)
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            if spec is None:
                raise ImportError(f"تعذر إنشاء مواصفات للإضافة {plugin_name}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            if plugin_name in sys.modules:
                importlib.reload(sys.modules[plugin_name])
            loaded_plugins.append(plugin_name)
        except Exception as e:
            error_msg = f"❌ فشل تحميل {plugin_name}: {str(e)}"
            print(error_msg)
            print(f"🔍 تفاصيل الخطأ:\n{traceback.format_exc()}")
            failed_plugins.append((plugin_name, str(e), traceback.format_exc()))
    return loaded_plugins, failed_plugins

async def auto_join_groups():
    try:
        userbot = await get_userbot(BOT_USERNAME)
        if not userbot:
            return 
        for group in GROUPS_TO_JOIN:
            try:
                await userbot.join_chat(group)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ فشل الانضمام إلى {group}: {e}")
    except Exception as e:
        print(f"❌ خطأ في الانضمام التلقائي: {e}")

async def setup_bot_commands():
    try:
        await app.set_bot_commands(
            commands=[
                BotCommand("start", "بدء تشغيل البوت"),
                BotCommand("vega", "سورس فيجا"),                        
                BotCommand("ping", "قياس سرعه البوت"),
                BotCommand("id", "لعرض الايدي خاص بك"),
            ],
            scope=BotCommandScopeAllPrivateChats(),
        )
        await app.set_bot_commands(
            commands=[BotCommand("play", "لتشغيل الاغنيه")],
            scope=BotCommandScopeAllGroupChats(),
        )
        await app.set_bot_commands(
            commands=[
                BotCommand("play", "Play requested song"),
                BotCommand("skip", "Skip to next track in queue"),
                BotCommand("pause", "Pause current song"),
                BotCommand("resume", "Resume paused song"),
                BotCommand("end", "Clear queue and leave voice chat"),
                BotCommand("shuffle", "Shuffle the playlist"),
                BotCommand("commands", "View available commands"),
                BotCommand("playmode", "Select playback mode"),
                BotCommand("settings", "Configure bot settings"),
            ],
            scope=BotCommandScopeAllChatAdministrators(),
        )
    except Exception as e:
        print(f"❌ خطأ في إعداد أوامر البوت: {e}")

async def send_startup_message():
    try:
        bot_info = await app.get_me()
        username = bot_info.username
        bot_id = bot_info.id
        mention = bot_info.mention            
        time_zone = pytz.timezone('Africa/Cairo')
        current_time = datetime.now(time_zone).strftime("%I:%M %p")     
        await app.send_video(
            chat_id=OWNER_ID,
            video="https://files.catbox.moe/68hpoe.mp4",
            caption=(
                f"<b> ㅤ\n• تم تشغيل بنجاح:\n• النظام : 𝗛𝘆𝗽𝗲𝗿𝗢𝘀\n\n"
                f"• اسم البوت :  {mention}\n"
                f"• معرف البوت :  @{username}\n"
                f"• ايدي البوت :  <code>{bot_id}</code>\n"
                f"• الوقت التشغيل : {current_time}</b>"
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("𝗛𝘆𝗽𝗲𝗿𝗢𝘀", url=f"https://t.me/vegaone")]]
            )
        )
    except Exception as e:
        print(f"❌ خطأ في إرسال رسالة بدء التشغيل: {e}")

async def init_assistants():
    try:
        if not STRING1:
            print("⚠️ لا توجد جلسات مساعدين")
            return        
        userbot = await get_userbot(BOT_USERNAME)
        if userbot:
            try:
                me = await userbot.get_me()
                assistants.append(1)
                assistantids.append(me.id)
                call = await get_call(BOT_USERNAME)
                bot_info = await app.get_me()
                if me.id != bot_info.id:
                    await send_start_to_bot(bot_info.username)
                await auto_join_groups()                
            except Exception as e:
                print(f"❌ خطأ في تهيئة الحساب المساعد: {e}")
        else:
            print("❌ فشل في الحصول على الحساب المساعد")
    except Exception as e:
        print(f"❌ خطأ في init_assistants: {e}")

async def init():
    try:
        if not STRING1:
            print("⚠️ تحذير: STRING1 غير موجود")
        await app.start()    
        loaded_plugins, failed_plugins = await load_plugins()
        bot_info = await app.get_me()
        username = bot_info.username
        bot_id = bot_info.id
        name = f"{bot_info.first_name} {bot_info.last_name or ''}".strip()
        print("\n" + "="*50)
        print("🎉 تم تشغيل البوت بنجاح!")
        print(f"🤖 البوت: {name} (@{username})")
        print(f"🆔 الايدي: {bot_id}")
        print(f"📊 الإضافات: {len(loaded_plugins)} محملة, {len(failed_plugins)} فاشلة")
        if failed_plugins:
            print(f"❌ الإضافات الفاشلة:")
            for plugin_name, error, tb in failed_plugins:
                print(f"   - {plugin_name}: {error}")
        await initialize_database()
        await send_startup_message()
        await setup_bot_commands()
        await init_assistants()                
        await idle()       
    except Exception as e:
        print(f"❌ خطأ فادح في التشغيل: {e}")
        print(f"🔍 تفاصيل الخطأ:\n{traceback.format_exc()}")   
    finally:
        try:
            print("🛑 جاري إيقاف البوت...")
            await app.stop()        
            userbot = await get_userbot(BOT_USERNAME)
            if userbot:
                await userbot.stop()
                print("✅ تم إيقاف الحساب المساعد")
        except Exception as e:
            print(f"❌ خطأ أثناء الإيقاف: {e}")

if __name__ == "__main__":
    print("🎵 بدء تشغيل بوت Harmony Music...")  
    try:
        asyncio.get_event_loop().run_until_complete(init())
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البوت بواسطة المستخدم")     
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        print(f"🔍 تفاصيل الخطأ:\n{traceback.format_exc()}")