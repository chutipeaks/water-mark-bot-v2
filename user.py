import asyncio
from bot import User
from pyrogram import filters , Client 
from pyrogram.types import Message
import re
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 


@User.on_message(filters.private & filters.text & filters.outgoing)
async def get_link(user:Client,message:Message):
    if message.text != '.get':
        return
    if message.reply_to_message:
        MSG = message.reply_to_message
    else:
        return await message.edit_text('Please Reply To A Message')
    if MSG.reply_markup is None:
        return await message.edit_text('Not Founded Keyboard')
    if MSG.reply_markup.keyboard is None:
        return 
    
    keyboard = MSG.reply_markup.keyboard
    original_keyboard_array =  np.array(keyboard)
    await message.edit_text('Process Started')
    await user.send_message(message.chat.id,'🎛 Buttons Editor')
    link:Message = await user.ask(message.chat.id, '/menulink')
    await asyncio.sleep(2)
    url = re.findall(r'(https?://[^\s]+)', link.text)
    if len(url) > 0:
        final_url_button_builder = f'{MSG.text} - {url.pop()}\n'
    else:
        final_url_button_builder = ''
    
    for key_board in keyboard:
        
        sub_url_button_builder = ''
        for sub_keyboard in key_board:
            if  not sub_keyboard in ['🎛 Buttons Editor','🛑 Stop Editor','📝 Posts Editor','💵 Balance','🔐 Admin'] and not sub_keyboard.endswith('Editand') and not 'Back' in sub_keyboard and not 'Menu' in sub_keyboard and not 'Button' in sub_keyboard and not 'Balance' in sub_keyboard.split() and not 'Admin' in sub_keyboard.split():
             #   await user.ask(message.chat.id, sub_keyboard)
            #    await asyncio.sleep(2)
                keyboard_message :Message =  await user.ask(message.chat.id, f'[ {sub_keyboard} ]')
                
                if keyboard_message.reply_markup is not None:
                    try:
                        if keyboard_message.reply_markup.keyboard is not None:
                            local_keyboard_array = np.array(keyboard_message.reply_markup.keyboard)   
                            if not np.array_equal(original_keyboard_array,local_keyboard_array):        
                                await asyncio.sleep(1)
                                link:Message = await user.ask(message.chat.id, '/menulink')
                                await asyncio.sleep(2)
                                url = re.findall(r'(https?://[^\s]+)', link.text)
                                if len(url) > 0:
                                    if sub_url_button_builder == '':
                                        sub_url_button_builder = f'{sub_keyboard} - {url.pop()}'
                                    else:
                                        sub_url_button_builder = sub_url_button_builder + f' && {sub_keyboard} - {url.pop()}'
                    except AttributeError:
                        pass
        final_url_button_builder = final_url_button_builder +'\n'+ sub_url_button_builder.rstrip().lstrip()
       # print(key_board)
    final_url_button_builder = final_url_button_builder.lstrip().rstrip()
    await message.edit_text('Process Finished')
    await user.send_message('me',final_url_button_builder)
    await user.send_message(message.chat.id,'🛑 Stop Editor')
    
