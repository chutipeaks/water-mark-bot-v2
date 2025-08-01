from pyrogram import idle
from bot import Bot #, User
import asyncio
import threading
from helpers.watermark_pdf_download_upload import thread_function
import traceback
from PIL import Image
from var import var
import os

r= "\u001b[31;1m"
a= "\u001b[32m"
y = "\u001b[33;1m"
b="\u001b[34;1m"
m="\u001b[35;1m"
c="\u001b[36;1m"

async def main():
    _footerimg = Image.open(var._footerimgpath)
    var._footerimg_w , var._footerimg_h = _footerimg.size
    var._footerimg_h = float(var._footerimg_h)
    var._footerimg_w = float(var._footerimg_w)
    data_file = open('data.txt','r',encoding='utf-8')
    var._data_aray  = data_file.read().split('\n')
    data_file.close()
      
    for dir in var.directory:
        os.makedirs(dir,exist_ok=True)
    await Bot.start()
  #  await User.start()
    print(y+f"----------------------- Service Started ---------------------")
    print(y+'                        Bot =>> {}'.format((await Bot.get_me()).username))
  #  print(y+'                        User Bot =>> {}'.format((await User.get_me()).first_name))
    try:
        threading.Thread(target=thread_function, args=(Bot,)).start()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    print(y+'---------------------------------------------------------------')
    await idle()
    print(y+f"----------------------- Service Stopped ---------------------")
    print(y+'                        Bot =>> {}'.format((await Bot.get_me()).username))
   # print(y+'                        User Bot =>> {}'.format((await User.get_me()).first_name))
    print(y+'---------------------------------------------------------------')
    await Bot.stop()
   # await  User.stop()

        

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('----------------------- Service Stopped -----------------------')
