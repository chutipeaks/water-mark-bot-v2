from helpers.watermark import watermark_pdf
from helpers.progress import progress_for_pyrogram
import os
import time
import  shutil
from pyrogram import Client ,enums
from pyrogram.types import Message
from helpers.queue import que
import asyncio
from helpers.add_link_pdf import add_link_pdf
from helpers.remove_image_annotatons import remove_uknown_image_annotations_main
from helpers.remove_watermark_texts import remove_watermark_text_main
from var import var
from datetime import datetime
from database.dbmain import get_all_db

logos = [ 'logo35.png','logo25.png','logo45.png','logo50.png','logo65.png','logo75.png','logo85.png']

def thread_function(bot:Client):
  asyncio.run(watermark_pdf_download_upload(bot))

def isSorted(l:list):
  length = len(l)
  i=1
  if length == 0:
    return False
  else:
    while i< length:
      if l[i] < l[i-1]:
        return False
      i=i+1
    return True


async def watermark_pdf_download_upload(bot:Client):
  with open('emoji.txt','r', encoding="utf-8") as f:
    emoji_file = f.read()
    emoji_file =  emoji_file.split('\n')
  global que
  while True:
    if que.empty():
      continue
    else:
  
      message:Message = que.get()
      down = await message.reply_text('Downloading.....',quote=True)

      soreted_check_list = []
      
      dt = datetime.now()
      ts = datetime.timestamp(dt)
      
      input_path = f'{var.directory[3]}/{ts}'
      os.makedirs(input_path,exist_ok=True)
      
      input_file_name = f'{input_path}/input.pdf'
      await message.download(
          input_file_name,
          progress=progress_for_pyrogram,
          progress_args=(
                        bot,
                        "📤 Downloading ... 📤\n",
                        down,
                        time.time()
                      )
      )
      settings = get_all_db()
      square_size = 300
      total_pages = None

      logiimgpostition = settings['watermark position']
      if settings['remove annotations']:
        remove_unkown_return = False
        await down.edit_text('Removing Annotations....')
        remove_unkown_return = await remove_uknown_image_annotations_main(input_file_name,input_path)

        if remove_unkown_return:
          input_file_name = remove_unkown_return 
          
      if settings['remove watermark text']:
        await down.edit_text('Removing Watermark Text....')
        remove_watermark_text_return = await remove_watermark_text_main(input_file_name,input_path)

        if remove_watermark_text_return:
          input_file_name = remove_watermark_text_return
        
      if settings['add watermark'] :
        await down.edit_text('Watermarking....\n\nTotal Pages : ⌛\nWatermarked pages : ⌛')
        add_watermark_return =  await watermark_pdf(down,logos[0], square_size,input_file_name,input_path,logiimgpostition)
        input_file_name = add_watermark_return
        await down.edit_text('Adding Link....')
        add_link_return  , total_pages = await add_link_pdf(input_file_name,square_size,input_path,logiimgpostition)
        input_file_name = add_link_return
        
      
      # thumbnail
      thumbnail = f"{input_path}/thumbnail.jpg"
      thumbnail = thumbnail if os.path.exists(thumbnail) else None

      # caption
      # compression
      
      output_file_name = input_file_name
      await down.edit_text('Uploading....')
      
      
      if message.caption is not None and settings['caption']:

        markdown_caption:str = message.caption
        split_caption_array = markdown_caption.split('\n')
        generating_caption = ''
        added_footer_text = False

        Header_Green = None
        Teacher_ame_Hand = ''
        for i in range(0,len(split_caption_array)):
            split_caption = split_caption_array[i]
            split_caption_final = split_caption.lstrip().rstrip()
            if len(split_caption_final) > 0:
              if split_caption_final.startswith(emoji_file[0]):# ❇️
                  generating_caption = generating_caption + f"--__**{split_caption_final}**__--\n\n"
                  soreted_check_list.append(i)
                  if Header_Green is None:
                    Header_Green = split_caption_final.replace(emoji_file[0],' ')
                    Header_Green = Header_Green.rstrip()
                    Header_Green = Header_Green.lstrip()
                  
              elif split_caption_final.startswith(emoji_file[1]):# 🔺
                  generating_caption = generating_caption + f'**{split_caption_final}**\n'
                  soreted_check_list.append(i)
                
              elif split_caption_final.startswith(emoji_file[2]):# ☝
                  generating_caption = generating_caption + f'__{split_caption_final}__\n'
                  soreted_check_list.append(i)
                  Teacher_ame_Hand = split_caption_final[1:]
                  Teacher_ame_Hand = Teacher_ame_Hand.rstrip()
                  Teacher_ame_Hand = Teacher_ame_Hand.lstrip()
                
              elif split_caption_final.startswith(emoji_file[3]):# 📌️
                  generating_caption = generating_caption + f'**{split_caption_final}**\n'
                  soreted_check_list.append(i)
              
          
              elif split_caption_final.startswith('(') and split_caption_final.endswith(')'):
                  generating_caption = f"{generating_caption}\n||__📄 Total Page : **{total_pages}**__||\n\n{var._footer_text}"
                  soreted_check_list.append(i)
                  added_footer_text  = True
                
              elif split_caption_final == '@ANYyScienceStudentHelpbot':
                  soreted_check_list.append(i)
            else:
              continue   
        
        if Header_Green is not None:

          Header_Green = Header_Green.replace('/',' ')

          while Header_Green.startswith('_') :
            Header_Green = Header_Green[1:]
          
          while Header_Green.startswith(var._data_aray[0]):
            Header_Green = Header_Green[3:]

          if Teacher_ame_Hand == '':
            new_file_name = f"./temp/{Header_Green}_@ANYyScienceStudentHelpbot.pdf"
          else:
            new_file_name = f"./temp/{Header_Green}_{Teacher_ame_Hand}_@ANYyScienceStudentHelpbot.pdf"
            
          new_file_name = new_file_name.replace(' ','_')
          try:
            os.rename(output_file_name,new_file_name)
            output_file_name = new_file_name
          except:
            pass
        else:
          new_file_name = output_file_name.replace(' ',"_")
          try:
            os.rename(output_file_name,new_file_name)
            output_file_name = new_file_name
          except:
            pass
          
        
        if not added_footer_text :
              generating_caption = f"{generating_caption}\n||__📄 Total Page : **{total_pages}**__||\n\n{var._footer_text}"
        
        
      
      if settings['caption']:
        final_caption = generating_caption
        parsemode = enums.parse_mode.ParseMode.MARKDOWN
        captionentities = None
      else:
        final_caption = None
        parsemode = None
        captionentities = None
      await message.reply_document(
              output_file_name,
              thumb=thumbnail ,
              caption= final_caption,#message.caption,
              caption_entities= captionentities,
              parse_mode=parsemode,
              quote=True,
              progress=progress_for_pyrogram,
              progress_args=(
                            bot,
                            "📤 Uploading ... 📤\n",
                            down,
                            time.time()
          ))
      await down.delete()
      shutil.rmtree(input_path,ignore_errors=True) 
      
      """try:
          os.remove(input_file_name)
      except:
          pass
        
      try:
        os.remove(thumbnail)
      except:
        pass
      try:
        os.remove(watermark_file_name)
      except:
        pass
      try:
        os.remove(output_file_name)
      except:
        pass"""
      
