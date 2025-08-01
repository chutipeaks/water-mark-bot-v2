from . import DB

def set_db(key,value):
    value =  int(value)
    DB.set(key,value)
    
def get_db(key):
    value = DB.get(key)
    if value:
        result = int(value) == 1
    else:
        result = False
        set_db(key,result)
        
    return result

def get_db_int(key):
    value = DB.get(key)
    if value:
        result = int(value)
    else:
        result = 2
        set_db(key,result)
    return result

def get_all_db():
    settings = {
        "remove annotations":get_db('removeannotations'),
        "remove watermark text":get_db('removewatermarktext'),
        "add watermark":get_db('addwatermark'),
        "watermark position":get_db_int('watermarkposition'),
        "caption":get_db('caption'),
    }
    return settings