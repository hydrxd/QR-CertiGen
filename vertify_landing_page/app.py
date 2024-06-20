from flask import Flask, render_template
import os
from PIL import Image, ImageDraw, ImageFont
import time

app = Flask(__name__)

@app.route('/<path:route>')
def render_certificate(route):
    if os.path.exists(os.path.join(app.root_path, 'static', route + '.png')):
        image_path = os.path.join(app.root_path, 'static', route + '.png')
        print(image_path)
    else:
        image_path = os.path.join(app.root_path, 'static', route + '.png')
    if not os.path.exists(image_path):
        return "Certificate not found", 404
    
    return render_template('certificate.html')

if __name__ == '__main__':
    app.run()
