from cv2 import cv2
from flask import Flask, request, jsonify
import pytesseract
import re
from pytesseract import Output
import spacy
from base64 import b64encode
from json import dumps
import numpy as np
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher
phrase_matcher = PhraseMatcher(nlp.vocab)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def process_image(path=None,keyword=None):
    if path == None:
       result = {'err': True, 'message': 'Path Can`t be empty', 'data':False}
       code = 403
       return result,code

    if keyword == None:
        result = {'err': True, 'message': 'keyword field reuired', 'data':False}
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

        # phrases = ['masalah korupsi']
        # patterns = [nlp(text) for text in phrases]
        # phrase_matcher.add('AI', None, *patterns)
        # sentence = nlp (result['text'].lower())
        # matched_phrases = phrase_matcher(sentence)
        # for match_id, start, end in matched_phrases:
        #     string_id = nlp.vocab.strings[match_id]  
        #     span = sentence[start:end]   
        #     print(match_id, string_id, start, end, span.text)

        result = {'text': resultOcr['text'], 'imageResult': ''}

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
                    base64_string = base64_bytes.decode('utf-8')
                    result['imageResult'] = base64_string


        if not result['imageResult']:
            result = {'err': True, 'message':'keyword '+keyword+' no match!', 'data': False}
            code = 404
            return result,code
        else:
            result = {'err': False, 'message':'successfully recognized image', 'data': result}
            code = 200
            return result,code
