from PyPDF2 import PdfWriter, PdfReader , Transformation
from PyPDF2.generic import AnnotationBuilder
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from var import var

pdfmetrics.registerFont(TTFont('iskole', './fonts/Iskoola Pota Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansSinhala', './fonts/NotoSansSinhala-Black.ttf'))


async def add_link_pdf(input_pdf_file:str,square_size,path,logiimgpostition:int):
    input_pdf = PdfReader(input_pdf_file)
    output = PdfWriter()
    
    total_pages  = len(input_pdf.pages)
    for PAGE in range(total_pages):
        inputpdf_page_to_be_merged = input_pdf.pages[PAGE]
        #sys.stdout.write(input_pdf)
        
        first_page_height = float(inputpdf_page_to_be_merged.mediabox.height)
        first_page_width = float(inputpdf_page_to_be_merged.mediabox.width)
        
        packet = io.BytesIO()
        c = Canvas(packet,pagesize=(first_page_width,first_page_height))

        draw_string = "https://t.me/ANYyScienceStudentHelpbot"
        draw_string_colors = [0,0,255]
        font_name = "Helvetica-BoldOblique"  #"Courier-Oblique" "Helvetica-BoldOblique" "Courier-Bold"
        font_size = 13

        string_width =  float(c.stringWidth(draw_string,font_name ,font_size))

        draw_string_x_value = (float(first_page_width)/2) -  (string_width/2)
        draw_string_y_value = first_page_height - font_size

       # rect_x1 = draw_string_x_value
      #  rect_y1 = draw_string_y_value 
     #   rect_x2 = rect_x1 + string_width + 2  # needs margin
       # rect_y2 = rect_y1 + font_size + 2  # needs margin


        c.setFillColorRGB(draw_string_colors[0],draw_string_colors[1],draw_string_colors[2]) #choose your font colour
        c.setFont(font_name, font_size) #choose your font type and font size
        c.drawString(draw_string_x_value,draw_string_y_value,text = draw_string) # write your text
        c.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        overlay = overlay_pdf.pages[0]
        
        Page_in_pdf = input_pdf.pages[PAGE]
        getwidth = overlay.mediabox.width
        getheight = overlay.mediabox.height
        matRixx= (Page_in_pdf.mediabox.width/2) - (getwidth  / 2)
        matRixy = (Page_in_pdf.mediabox.height/2) - (getheight / 2)
        """Page_in_pdf.mergeRotatedTranslatedPage(
              overlay, 
              inputpdf_page_to_be_merged.get('/Rotate') or 0, 
              float(getwidth/2), 
              float(getwidth/2)
            )"""
        overlay.add_transformation(Transformation().rotate(inputpdf_page_to_be_merged.get('/Rotate') or 0).translate(float(matRixx), 
              float(matRixy)))
        Page_in_pdf.merge_page(overlay) 
       # Page_in_pdf.compress_content_streams()
        output.add_page(Page_in_pdf)

        page_height = float(Page_in_pdf.mediabox.height)
        page_width = float(Page_in_pdf.mediabox.width)
        
        x = (page_width - square_size)/2

        if logiimgpostition == 1:
            y = (page_height*(5/6)) - (square_size/2)
        elif logiimgpostition == 2:
            y = (page_height - square_size)/2
        elif logiimgpostition == 3:
            y = (page_height/6) - (square_size/2)
        else:
            y = (page_height - square_size)/2
    
        watermark_annotation_link = AnnotationBuilder.link(
          rect=(x,y,x+square_size,y+square_size),
          url="https://t.me/ANYyScienceStudentHelpbot",
        )
        output.add_annotation(page_number=PAGE, annotation=watermark_annotation_link)
        
        string_annotation_link = AnnotationBuilder.link(
          rect=((page_width - string_width)/2,page_height,((page_width - string_width)/2)+string_width,page_height - font_size),
          url="https://t.me/ANYyScienceStudentHelpbot",
        )
        output.add_annotation(page_number=PAGE, annotation=string_annotation_link)
        
        
        #f =  open ('writedata.txt','w')
        #f.write(str(f'footer img height = {var._footerimg_h} footer img width = {var._footerimg_w}')+'\n\n')
       # f.write(f'page width = {page_width} rectangle height = {(page_width/var._footerimg_w)*var._footerimg_h}'+'\n\n')
        annotation_link = AnnotationBuilder.link(
            rect=(0,0,page_width,(page_width/var._footerimg_w)*var._footerimg_h),
            url="https://t.me/ANYyScienceStudentHelpbot",
        )
      #  f.close() 
        output.add_annotation(page_number=PAGE, annotation=annotation_link)
        

    """split_input_pdf =  input_pdf.split('/')
    
    output_file_name = split_input_pdf[len(split_input_pdf)-1]
    
    output_file_name = output_file_name.replace('attachment','')
    while output_file_name.startswith('-'):
        output_file_name = output_file_name[1:]"""
    return_path = f'{path}/add_link.pdf'

    with open( return_path, "wb") as f:
        output.write(f)
    return  return_path , total_pages 
