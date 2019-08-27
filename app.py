from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import random
import string
import os
from flask import Flask, render_template, request,redirect,url_for
import sys
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
app = Flask(__name__)
app.config['DEBUG'] = True
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('weather.html', visible="hidden")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['POST'])
def post():
    if request.form['captcha'] == 'Upload':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "upload.png"))
        sayi = random.randint(1000, 9999)
        deneme=ocr('static/images/upload.png')
        return render_template('weather.html',captcha=deneme,visible="visible", src='{}{}'.format('static/images/upload.png?rnd=', sayi))
    if request.form['captcha'] == 'Create Captcha':
        ad = request.form['text']
    elif request.form['captcha'] =='Create Random Captcha':
        digits = "".join([random.choice(string.digits) for i in range(1,3)])
        chars = "".join([random.choice(string.ascii_letters) for i in range(1,3)])
        ad=chars+digits
    img = Image.new('RGB', (300, 100), color=(0, 0, 0))
    img2 = Image.new('RGB', (300, 100), color=(0, 0, 0))
    img3 = Image.new('RGB', (300, 100), color=(0, 0, 0))
    fnt = ImageFont.truetype('/font/arial.ttf', 80)
    d = ImageDraw.Draw(img)
    d1 = ImageDraw.Draw(img2)
    d2 = ImageDraw.Draw(img3)
    d1.text((50, 15), ad, font=fnt, fill=(255, 255, 255))
    d.text((50, 15), ad, font=fnt, fill=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((random.randint(1, 300), random.randint(1, 100), random.randint(1, 300), random.randint(1, 100)),
              fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)),
              width=random.randint(5, 15))
    draw.line((random.randint(1, 300), random.randint(1, 100), random.randint(1, 300), random.randint(1, 100)),
              fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)),
              width=random.randint(5, 15))
    draw.line((random.randint(1, 300), random.randint(1, 100), random.randint(1, 300), random.randint(1, 100)),
              fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)),
              width=random.randint(5, 15))
    draw.line((random.randint(1, 300), random.randint(1, 100), random.randint(1, 300), random.randint(1, 100)),
              fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)),
              width=random.randint(5, 15))
    draw.arc((random.randint(1, 100), random.randint(1, 50), random.randint(100, 250), random.randint(50, 100)), 0, 360,
             fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)))
    draw.arc((random.randint(1, 100), random.randint(1, 50), random.randint(100, 250), random.randint(50, 100)), 0, 360,
             fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)))
    draw.arc((random.randint(1, 100), random.randint(1, 50), random.randint(100, 250), random.randint(50, 100)), 0, 360,
             fill=(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)))
    img2.save('static/images/img2.png', 'PNG')
    img.save('static/images/img1.png', 'PNG')
    img3.save('static/images/img3.png', 'PNG')
    img = plt.imread("static/images/img1.png")
    img2 = plt.imread("static/images/img2.png")
    fark = img - img2
    plt.imsave('static/images/img3.png', fark)
    sonuc = img - fark
    plt.imsave("static/images/sonuc.png", sonuc)
    img = Image.open('static/images/sonuc.png')
    result = pytesseract.image_to_string(img)
    sayi = random.randint(1000, 9999)
    return render_template('weather.html', captcha=result, visible="visible", src='{}{}'.format('static/images/img1.png?rnd=', sayi))

def a(img, letter):
    A = img.load()
    B = letter.load()
    mx = 1000000
    max_x = 0
    x = 0
    for x in range(img.size[0] - letter.size[0]):
        _sum = 0
        for i in range(letter.size[0]):
            for j in range(letter.size[1]):
                _sum = _sum + abs(A[x+i, j][0] - B[i, j][0])
        if _sum < mx :
            mx = _sum
            max_x = x
    return mx, max_x
def ocr (im, threshold = 200, alphabet = "0123456789abcdef"):
    img = Image.open(im)
    img = img.convert("RGB")
    box = (8, 8, 58, 18)
    img = img.crop(box)
    pixdata = img.load()
    letters = Image.open('static/images/letters.bmp')
    ledata = letters.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] > threshold) \
                    and (pixdata[x, y][1] > threshold) \
                    and (pixdata[x, y][2] > threshold):

                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)
    counter = 0
    old_x = -1

    letterlist = []

    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y][0] != 0 :
                black = False
                break
        if black :
            if True :
                box = (old_x + 1, 0, x, 10)
                letter = letters.crop(box)
                t = a(img, letter)
                letterlist.append((t[0], alphabet[counter], t[1]))
            old_x = x
            counter += 1

    box = (old_x + 1, 0, 140, 10)
    letter = letters.crop(box)
    t = a(img, letter)
    letterlist.append((t[0], alphabet[counter], t[1]))

    t = sorted(letterlist)
    t = t[0:5]  # 5-letter captcha

    final = sorted(t, key=lambda e: e[2])
    answer = ""
    for l in final:
        answer = answer + l[1]
    return answer



