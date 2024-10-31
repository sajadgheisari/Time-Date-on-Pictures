from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import io

app = Flask(__name__)

# تاریخ و ساعت اولیه را تنظیم کنید
initial_date = datetime(2023, 11, 1, 12, 0)  # برای مثال 1 نوامبر 2023 ساعت 12:00

# مسیر فونت (در صورت نیاز آن را تغییر دهید)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    if not file:
        return "No image uploaded", 400

    # باز کردن تصویر
    image = Image.open(file.stream)
    draw = ImageDraw.Draw(image)

    # تنظیم تاریخ و ساعت برای این تصویر
    timestamp = initial_date + timedelta(minutes=1)  # این قسمت را تغییر دهید که ساعت درست محاسبه شود
    timestamp_text = timestamp.strftime("%Y-%m-%d %H:%M")

    # تنظیم فونت
    font = ImageFont.truetype(font_path, 40)

    # اضافه کردن متن تاریخ و ساعت روی تصویر
    text_position = (10, 10)
    draw.text(text_position, timestamp_text, font=font, fill="white")

    # ذخیره تصویر در حافظه برای ارسال به کلاینت
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
