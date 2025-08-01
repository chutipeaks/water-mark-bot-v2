from skimage import io
from pdf2image import convert_from_path 
from fitz import Document ,Pixmap
import numpy as np
import img2pdf
import warnings
from PIL import Image
from multiprocessing import Pool
import os
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

#img = cv2.imread('gradient.png',0)
#ret, thresh1 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)




# imgs = io.imread('./test.png')
# io.imsave('./hh.png',imgs)
# imgs = np.array(imgs)
# print(imgs.shape)
# r = []
# g = []
# b = []
# alpha = []

def judge(x,y):
    temp = -(600.0/1575.0) * x
    if y > 1350 + temp and y < 1500 + temp:
        return True
    else:
        return False

# for  i in range(imgs.shape[0]):
#     for j in range(imgs.shape[1]):
#         if not judge(j,i):
#             continue
#         if imgs[i][j][1] > 100 and imgs[i][j][1] < 250 and imgs[i][j][2] > 100 and imgs[i][j][2] < 250:
#             imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 255
#         if imgs[i][j][1] < 10 and imgs[i][j][2] < 100:
#             imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 0 

# io.imsave('./hh.png',imgs)
# print(r)
# print(g)
# print(b)
# print(alpha)

def handle(imgs):
    for i in range(imgs.shape[0]):
        for j in range(imgs.shape[1]):
            r, g, b = imgs[i][j][0], imgs[i][j][1], imgs[i][j][2]
            if r > 175 and g > 175 and b > 175:
                imgs[i][j][0] = imgs[i][j][1] = imgs[i][j][2] = 255
    return imgs

def multi_run_wrapper(args):
    return handle_images(*args)

def handle_images(index,img,img_path):
    print(f'{index} image handling...')
    img = np.array(img)
    img = handle(img)
    io.imsave(img_path, img)
    print(f'{index} image handle ended.')
    return img_path
    # break

"""def extract_iamges (filename:str,img_path:str):
    Doc = Document(filename)
    parameterlist = []
    index = 0
    for page in Doc:
        image:Pixmap  = page.get_pixmap() 
       # image.save(f'{img_path}/{index}.jpg')
        index = index + 1
        parameterlist.append((index,image,f"{img_path}/{index}.jpg"))
    return parameterlist"""
        

async def remove_watermark_text_main(filename,path):
    index = 0  
    img_path = f'{path}/images'
    os.makedirs(img_path,exist_ok=True)
    

    images = convert_from_path(filename,200,poppler_path=f'{os.path.abspath(os.getcwd())}/poppler/bin',
                               jpegopt={
                                    "quality": 100,
                                    "progressive": True,
                                    "optimize": True
                                }
    )

    parameterlist = []
 #   images = np.array(images)
    for img in images:
        index = index +1
        parameterlist.append((index,img,f"{img_path}/{index}.jpg"))
        


    pool = Pool(len(images))
    print(f'Starting {len(images)} images removig watermark')
    images_path = pool.map(multi_run_wrapper, parameterlist)
    if None in images_path:
        final_path = []
        for i_path in images_path:
            if i_path is not None:
                final_path.append(i_path)
        images_path = final_path
    print('Process ended')
    return_file_name = f'{path}/remove_watermark_text.pdf'    
    try:
        with open(return_file_name,"wb") as f:
            f.write(img2pdf.convert(images_path))
        return return_file_name
    except:
        return False
    

"""a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))"""