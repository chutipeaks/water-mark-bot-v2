from pyrogram import Client, filters
from pyrogram.types import Message 
#from bot import Bot

@Client.on_message(filters.command('start') & filters.private,group=-1)
async def start_msg(bot:Client, message:Message):
    await message.reply_text("I'm alive")