from pyrogram.types import Message
from fitz import Rect , Document , Matrix
from var import var

  
   
async def watermark_pdf(down:Message,logo_name ,square_size,input_file_name,path,logiimgpostition:int):
    
    doc = Document(input_file_name)
    pdf:Document = doc
    
    logoimg = open(f'./helpers/logo/{logo_name}', "rb").read()
    footerimg = open(var._footerimgpath , "rb").read()
    

    zoom = 4 # to increase the resolution
    
    mat = Matrix(zoom, zoom)
    
    page = doc.load_page(0)  # number of page
    pix = page.get_pixmap(matrix = mat)
    pix.save(f"{path}/thumbnail.jpg", "jpeg")

    
    
    for i in range(0, pdf.page_count):
        page = pdf[i]
        x = (page.mediabox.width - square_size)/2

        if logiimgpostition == 1:
            y = (page.mediabox.height/6) - (square_size/2)
        elif logiimgpostition == 2:
            y = (page.mediabox.height - square_size)/2
        elif logiimgpostition == 3:
            y = (page.mediabox.height*(5/6)) - (square_size/2)
        #height = page.mediabox.width
        
        rect = Rect(x,y,x+square_size,y + square_size)
        if not page.is_wrapped:
            page.wrap_contents()
    
        page.insert_image(Rect(0,page.mediabox.height - ((page.mediabox.width/var._footerimg_w)*var._footerimg_h),page.mediabox.width,page.mediabox.height), stream=footerimg )
        page.insert_image(rect, stream=logoimg)
        if i%5 == 0 or i == 0 or i == pdf.page_count:
            await down.edit_text(f'Watermarking....\n\nTotal Pages : {pdf.page_count}\nWatermarked pages : {i}')
        

    return_file_name = f'{path}/watermark.pdf'
    doc.save(return_file_name,garbage=3, deflate=True)
    return return_file_name