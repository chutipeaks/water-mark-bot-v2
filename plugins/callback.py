from pyrogram import Client, filters
from pyrogram.types import  CallbackQuery
from database.dbmain import set_db
from helpers.generate_reply_markup_settings import generate_reply_markup_settings

@Client.on_callback_query(filters.regex("(addwatermark|caption|removewatermarktext|removeannotations)\s(True|False)"))
async def settings_call_back_query(client, callback:CallbackQuery):
    callbackdata = callback.data.split()
    set_db(callbackdata[0],True if callbackdata[1] == 'True' else False)
    await callback.answer()
    await generate_reply_markup_settings(callback.message)

@Client.on_callback_query(filters.regex("(watermarkposition)\s(1|2|3)"))
async def watermarkposition_call_back_query(client, callback:CallbackQuery):
    callbackdata = callback.data.split()
    set_db(callbackdata[0],callbackdata[1])
    await callback.answer()
    await generate_reply_markup_settings(callback.message)
    