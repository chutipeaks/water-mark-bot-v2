from pyromod import listen
from pyrogram import Client
from var import var

    
Bot = Client(
   # test_mode=True,
    name= var.BOT_SESSION_NAME,
    api_id= var.BOT_APP_ID,
    api_hash= var.BOT_API_HASH,
    bot_token= var.BOT_BOT_TOKEN,
    plugins=dict(root="plugins")

)

User = Client(
    name='userbot',
    api_id=var.USER_APP_ID,
    api_hash= var.USER_API_HASH,
    in_memory=False,
    session_string=var.STRING_SESSION,
    test_mode=True
)