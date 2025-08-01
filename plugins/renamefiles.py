from pyrogram import Client, filters
from pyrogram.types import Message
import os
from helpers.progress import progress_for_pyrogram
import time
#from bot import Bot



@Client.on_message(filters.text & filters.private)
async def rename_files(bot:Client, message:Message):
  if message.reply_to_message:
    document = message.reply_to_message
    if document.document is not None:
      down = await message.reply_text('Downloading.....',quote=True)
      file_name = f"./renametemp/{document.document.file_name}"
      await document.download(
          file_name,
          progress=progress_for_pyrogram,
          progress_args=(
                        bot,
                        "📤 Downloading ... 📤\n",
                        down,
                        time.time()
                      )
        )
      output_file_name = f"./renametemp/{message.text.rstrip().lstrip()}_@ANYyScienceStudentHelpbot.pdf".replace(' ','_')
      try:
        os.rename(file_name,output_file_name)
      except Exception as e:
        return await message.reply_text(f'Sorry !\n\nFile Rename fail : {e}')
      await down.edit_text('Downloading thumbnail....')
      await message.reply_text('👇')
      if document.document.thumbs[0].file_id is not None:
        thumbnail = await bot.download_media(document.document.thumbs[0].file_id)
      else:
        thumbnail = None
      await down.edit_text('Uploading Document....')  
      await document.reply_document(
                output_file_name,
                thumb=thumbnail,
                caption= document.caption,#message.caption,
                caption_entities =  document.caption_entities,
                quote=True,
                progress=progress_for_pyrogram,
                progress_args=(
                              bot,
                              "📤 Uploading ... 📤\n",
                              down,
                              time.time()
              ))
      await message.reply_text('👆')
      await down.delete()
      try:
        os.remove(output_file_name)
        os.remove(thumbnail)
      except:
        pass