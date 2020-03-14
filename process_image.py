from cv2 import cv2
import pytesseract


def process_image(path=None):
    if path == None:
       return {'err': True, 'message': 'Path Can`t be empty', 'data':''}
    else:
        img = cv2.imread(path)
        result = pytesseract.image_to_string(img)
        return {'err': False, 'message':'successfully recognized image', 'data': result}