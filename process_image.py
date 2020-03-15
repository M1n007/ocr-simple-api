from cv2 import cv2
import pytesseract

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def process_image(path=None):
    if path == None:
       return {'err': True, 'message': 'Path Can`t be empty', 'data':''}
    else:
        img = cv2.imread(path)
        gray = get_grayscale(img)
        threshs = thresholding(gray)
        custom_config = r'--psm 6'
        result = pytesseract.image_to_string(threshs, config=custom_config)
        return {'err': False, 'message':'successfully recognized image', 'data': result}