from cv2 import cv2
import pytesseract


def process_image(path=None):
    if path == None:
       return {'err': True, 'message': 'Path Can`t be empty', 'data':''}
    else:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = pytesseract.image_to_string(gray)
        return {'err': False, 'message':'successfully recognized image', 'data': result}