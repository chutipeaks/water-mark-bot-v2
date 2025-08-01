from pyrogram.types import Message ,InlineKeyboardButton ,InlineKeyboardMarkup
from database.dbmain import get_all_db
from var import var

async def generate_reply_markup_settings(message:Message):
    settings = get_all_db()
    reply_markup=\
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            f"Remove Annotaions : {var.on_off_switch_data['on'] if settings['remove annotations'] else var.on_off_switch_data['off']}",
                            callback_data=f"removeannotations {str(settings['remove annotations'] is False)}"
                        )
                    ],
                    [
                        InlineKeyboardButton(  # Opens a web URL
                            f"Remove Watermark Text : {var.on_off_switch_data['on'] if settings['remove watermark text'] else var.on_off_switch_data['off']}",
                            callback_data=f"removewatermarktext {str(settings['remove watermark text']  is False)}"
                        )
                    ],
                    [
                        InlineKeyboardButton(  # Opens a web URL
                            f"Caption : {var.on_off_switch_data['on'] if settings['caption'] else var.on_off_switch_data['off']}",
                            callback_data=f"caption {str(settings['caption'] is False)}"
                        )
                    ],
                    [
                        InlineKeyboardButton(  # Opens a web URL
                            f"Add Watermark : {var.on_off_switch_data['on'] if settings['add watermark'] else var.on_off_switch_data['off']}",
                            callback_data=f"addwatermark {str(settings['add watermark'] is False)}"
                        )
                    ]
                ]
    
    if settings['add watermark']:
        uppertext = "1"
        middletext = "2"
        downtext = "3"
        if settings["watermark position"] == 1:
            uppertext = "1️⃣"
        elif settings["watermark position"] == 2:
            middletext = "2️⃣"
        elif settings["watermark position"] == 3:
            downtext = "3️⃣"
        positionbuttons =\
            [
                InlineKeyboardButton(
                    uppertext,
                    callback_data=f"watermarkposition 1"
                ),
                InlineKeyboardButton(
                    middletext,
                    callback_data=f"watermarkposition 2"
                ),
                InlineKeyboardButton(
                    downtext,
                    callback_data=f"watermarkposition 3"
                )
            ]
        reply_markup.append(positionbuttons)
    try:
        await message.edit_text("Settings",reply_markup=InlineKeyboardMarkup(reply_markup))
    except Exception as e:
        print(e)