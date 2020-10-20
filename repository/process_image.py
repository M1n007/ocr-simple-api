from cv2 import cv2
from flask import Flask, request, jsonify
import pytesseract
import re
from pytesseract import Output
from base64 import b64encode, b64decode
from json import dumps
import nltk
from nltk.tokenize import word_tokenize
import difflib


sm = difflib.SequenceMatcher(None)


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def process_image(path=None,keyword=None,score=None):
    score_data = 0

    if score == None:
        score_data = 0.1
    else:
        score_data = score
    
    if path == None:
       result = {'err': True, 'message': 'Path Can`t be empty', 'data':False}
       code = 403
       return result,code

    if keyword == None:
        result = {'err': True, 'message': 'keyword field required', 'data':False}
        code = 403

        return result,code

    

    else:
        
        img = cv2.imread(path)
        overlay = img.copy()

        gray = get_grayscale(img)
        threshs = thresholding(gray)
        custom_config = r'--psm 6'
        resultOcr = pytesseract.image_to_string(threshs, output_type=Output.DICT)
        d = pytesseract.image_to_data(img, output_type=Output.DICT)

        text_ocr_result = resultOcr['text']
        formatted_ocr_result = re.sub('[^a-zA-Z]', ' ', text_ocr_result)
        formatted_ocr_result = re.sub(r'\s+', ' ', formatted_ocr_result)

        sm.set_seq2(keyword.lower())

        lasResultSimiliarity = []

        for x in word_tokenize(formatted_ocr_result):
            sm.set_seq1(x.lower())
            if sm.ratio() >= float(score_data):
                lasResultSimiliarity.append({x.lower():sm.ratio()})


        result = {'text': resultOcr['text'], 'match_result': lasResultSimiliarity, 'image_result': ''}

        all_word_length = len(d['text'])
        for i in range(all_word_length):
            match = re.search(r"\b%s\b" % keyword,d['text'][i].lower(),re.IGNORECASE)
            if match:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (64, 230, 61, 0.35), cv2.FILLED)
                    alpha = 0.4
                    image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
                    _, buffer = cv2.imencode('.png', image_new)
                    png_as_text = b64encode(buffer)
                    base64_bytes = b64encode(png_as_text)
                    base64_string_last_result = b64decode(base64_bytes)
                    last_result = base64_string_last_result.decode('utf-8')
                    result['image_result'] = last_result


        if not result['image_result']:
            result = {'err': True, 'message':'keyword '+keyword+' no match!', 'data': False}
            code = 404
            return result,code
        else:
            result = {'err': False, 'message':'successfully recognized image', 'data': result}
            code = 200
            return result,code
