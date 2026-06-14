import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from info import API_ID, API_HASH, BOT_TOKEN, ADMINS, AUTH_CHANNEL, PICS, DATABASE_URL, DATABASE_NAME

bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client[DATABASE_NAME]
movies_col = db["movies"] # MongoDB ထဲက ရုပ်ရှင် collection နာမည်

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (f"✨ **မင်္ဂလာပါ {message.from_user.mention} ဗျာ။**\n\n"
            f"ကျွန်တော်သည် **Movie Finder** ဖြစ်ပါတယ်တဗျာ။\n\n"
            f"လူကြီးမင်းတို့ ရှာဖွေလိုသော ရုပ်ရှင်ဇာတ်ကားများကို မမေမေတို့ရဲ့ Chat Group တွင် အလွယ်တကူ တောင်းဆိုရှာဖွေနိုင်ပါပြီ။ 🥰")
    
    buttons = [
        [InlineKeyboardButton("➕ Add Me To Your Chat ➕", url=f"http://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("Search 🔎", switch_inline_query_current_chat=""), InlineKeyboardButton("Channel 🔊", url="https://t.me/m33t22moviefinder_bot")],
        [InlineKeyboardButton("Help 🕸️", callback_data="help"), InlineKeyboardButton("About ✨", callback_data="about")]
    ]
    
    if PICS:
        await message.reply_photo(photo=PICS[0], caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

print("Bot ကြီး အောင်မြင်စွာ လည်ပတ်နေပါပြီ...")
bot.run()
