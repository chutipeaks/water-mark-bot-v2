import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.queue import que
#from bot import Bot

@Client.on_message(filters.document & filters.private)
async def document_filter(bot:Client, message:Message):
  global que
  que.put(message)
  try:
    delmessage = await message.reply_text('Added to Que Success ✅',quote=True)
    await asyncio.sleep(3)
    await delmessage.delete()
  except:
    pass
  