from pyrogram import Client, filters
from pyrogram.types import Message 
from helpers.generate_reply_markup_settings import generate_reply_markup_settings

@Client.on_message((filters.command('setting') | filters.regex(r'^setting$')) & filters.private, group=-1)
async def settings_msg(bot:Client, message:Message):
    process = await message.reply_text('Processing settings....')
    await generate_reply_markup_settings(process)