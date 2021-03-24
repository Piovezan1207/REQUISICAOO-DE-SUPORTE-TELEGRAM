import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def criar_QR(sala,link):
    url = str(link) + '/home?sala=' + sala

    payload = {'cht': 'qr', 'chs': '300x300','chl': url}
    r = requests.get('https://chart.googleapis.com/chart?', params = payload)
    arquivo =  "QR.png"
    file = open(arquivo, "wb")
    file.write(r.content)
    file.close()

    fundo = Image.open('qr_code/fundo.jpg')
    draw = ImageDraw.Draw(fundo)
    font = ImageFont.truetype("qr_code/arial.ttf", 38)
    qr = Image.open(arquivo)
    draw.text((810, 450),sala,(0,0,0),font=font)
    fundo.paste(qr, (330, 120))
    fundo.save(arquivo,"png")


    
    
    