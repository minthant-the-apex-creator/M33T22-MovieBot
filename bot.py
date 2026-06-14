import os
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from info import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, DATABASE_NAME, PICS

bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client[DATABASE_NAME]
movies_col = db["movies"] # MongoDB ထဲက မင်းရဲ့ ရုပ်ရှင် Collection နာမည်

# --- Start Command ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (f"✨ **မင်္ဂလာပါ {message.from_user.mention} ❤️🙏🏻။**\n\n"
            f"ကျွန်တော်သည် **Movie Finder** ဖြစ်ပါတယ်ဗျာ။\n\n"
            f"လူကြီးမင်းတို့ ရှာဖွေလိုသော ရုပ်ရှင်ဇာတ်ကားများကို မင်မင်တို့ရဲ့ Chat Group တွင် အလွယ်တကူ တောင်းဆိုရှာဖွေနိုင်ပါပြီ။ 🥰")
    
    buttons = [
        [InlineKeyboardButton("➕ Add Me To Your Chat ➕", url=f"http://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("Search 🔎", switch_inline_query_current_chat=""), InlineKeyboardButton("Channel 🔊", url="https://t.me/m33t22moviefinder_bot")],
        [InlineKeyboardButton("Help 🕸️", callback_data="help"), InlineKeyboardButton("About ✨", callback_data="about")]
    ]
    
    if PICS:
        await message.reply_photo(photo=PICS[0], caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# --- Auto Filter (ရုပ်ရှင်အလိုအလျောက် ရှာပေးသည့်စနစ်) ---
@bot.on_message(filters.text & filters.group)
async def group_filter(client, message):
    query = message.text.strip()
    
    # စာလုံးအရှည် ၂ လုံးထက်နည်းရင် ရှာမပေးပါ (စာရိုက်မှားတာတွေ မရှာမိအောင် ကာကွယ်ခြင်း)
    if len(query) < 2:
        return

    # MongoDB ထဲမှာ ရုပ်ရှင်နာမည်ကို စာလုံးအကြီးအသေးမရွေး (Case-insensitive) လိုက်ရှာခြင်း
    search_pattern = re.compile(query, re.IGNORECASE)
    results = await movies_col.find({"file_name": search_pattern}).to_list(length=10)

    if not results:
        # ရုပ်ရှင်ရှာမတွေ့ပါက ဘာမှပြန်မလုပ်ဘဲ ငြိမ်နေမည် သို့မဟုတ် message ပြန်မည်
        return

    # ရုပ်ရှင်တွေ့ပါက ခလုတ် (Button) ပုံစံဖြင့် လင့်ခ်များကို ထုတ်ပေးခြင်း
    buttons = []
    for movie in results:
        # မင်းရဲ့ Database တည်ဆောက်ပုံအရ file_name နှင့် file_link (သို့မဟုတ် file_id) ကို လှမ်းယူပါမည်
        movie_name = movie.get("file_name", "Unknown Movie")
        movie_link = movie.get("file_link", "#") 
        
        buttons.append([InlineKeyboardButton(f"🎬 {movie_name}", url=movie_link)])

    await message.reply_text(
        text=f"🔍 **မင်းရှာဖွေနေတဲ့ '{query}' အတွက် ရလဒ်များကို အောက်တွင် နှိပ်ပြီး ရယူနိုင်ပါပြီဗျာ ကလစ်နှိပ်လိုက်ပါ 👇**",
        reply_markup=InlineKeyboardMarkup(buttons),
        reply_to_message_id=message.id
    )

print("Bot ကြီး လုံးဝအသစ်သီးသန့် စနစ်ဖြင့် အောင်မြင်စွာ လည်ပတ်နေပါပြီ...")
bot.run()
