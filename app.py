from flask import Flask,request,jsonify
import easyocr
import re
import boto3
import io
from PIL import Image
from urllib.parse import urlparse
from googletrans import Translator
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
reader = easyocr.Reader(['en','hi'])
s3 = boto3.client('s3', 
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

@app.route('/imageOcr',methods=['POST'])
def ocr():
    print('req',request.json)
    image_url = request.json['imageurl']

    print('url',image_url)
    translator = Translator()


    parsed_url = urlparse(image_url)

   
    bucket = parsed_url.netloc.split('.')[0]
    key = parsed_url.path.lstrip('/')

    print('bucket',bucket,key)

    s3_res = s3.get_object(Bucket=bucket, Key = key)
    image_data = s3_res['Body'].read()

    image = Image.open(io.BytesIO(image_data))

    result = reader.readtext(image)

    text_output = [{'text': text[1], 'confidence': text[2]} for text in result]


    for item in text_output:
            if item['text'].strip():  
                detected_lang = translator.detect(item['text']).lang
                if detected_lang == 'hi':  
                    translated = translator.translate(item['text'], src='hi', dest='en')
                    item['translated_text'] = translated.text  


    return jsonify(text_output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
