import os
import re
import http.server
import socketserver
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from info import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, DATABASE_NAME

bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client[DATABASE_NAME]
movies_col = db["movies"] # MongoDB ထဲက မင်းရဲ့ ရုပ်ရှင် Collection နာမည်

# --- Render Port Scan ကာကွယ်ရန် Fake Server ---
def run_fake_server():
    PORT = int(os.environ.get("PORT", 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

threading.Thread(target=run_fake_server, daemon=True).start()


# --- Start Command (ပုံစနစ် လုံးဝမပါဘဲ စာသားသက်သက်သာ ပို့မည့်စနစ်) ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (f"✨ **မင်္ဂလာပါ {message.from_user.mention} ဗျာ။**\n\n"
            f"ကျွန်တော်သည် **Movie Finder** ဖြစ်ပါတယ်ဗျာ။\n\n"
            f"လူကြီးမင်းတို့ ကြည်ရှု့လိုသော ရုပ်ရှင်ဇာတ်ကားများကို မင်မင်တို့ရဲ့ Chat Group တွင် အလွယ်တကူ တောင်းဆိုရှာဖွေနိုင်ပါပြီ။ 🥰")
    
    buttons = [
        [InlineKeyboardButton("➕ Add Me To Your Chat ➕", url=f"http://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("Search 🔎", switch_inline_query_current_chat=""), InlineKeyboardButton("Channel 🔊", url="https://t.me/m33t22moviefinder_bot")],
        [InlineKeyboardButton("Help 🕸️", callback_data="help"), InlineKeyboardButton("About ✨", callback_data="about")]
    ]
    
    # reply_text ကိုသုံးပြီး စာသားနှင့် ခလုတ်များကိုသာ သန့်သန့်လေး ပို့ပေးမည် ဖြစ်သည်
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))


# --- Auto Filter (Group ထဲတွင် ရုပ်ရှင်အလိုအလျောက် ရှာပေးသည့်စနစ်) ---
@bot.on_message(filters.text & filters.group)
async def group_filter(client, message):
    query = message.text.strip()
    
    if len(query) < 2:
        return

    search_pattern = re.compile(query, re.IGNORECASE)
    results = await movies_col.find({"file_name": search_pattern}).to_list(length=10)

    if not results:
        return

    buttons = []
    for movie in results:
        movie_name = movie.get("file_name", "Unknown Movie")
        movie_link = movie.get("file_link", "#") 
        buttons.append([InlineKeyboardButton(f"🎬 {movie_name}", url=movie_link)])

    await message.reply_text(
        text=f"🔍 **မင်းရှာဖွေနေတဲ့ '{query}' အတွက် ရလဒ်များကို အောက်တွင် နှိပ်ပြီး ရယူနိုင်ပါပြီဗျာ ကလစ်နှိပ်လိုက်ပါ 👇**",
        reply_markup=InlineKeyboardMarkup(buttons),
        reply_to_message_id=message.id
    )

print("Bot ကြီး လုံးဝပုံစနစ်မပါဘဲ အောင်မြင်စွာ လည်ပတ်နေပါပြီ...")
bot.run()
