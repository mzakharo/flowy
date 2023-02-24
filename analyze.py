import pytesseract as pyt
import cv2
import numpy as np
import os
import imutils
import easyocr
import datetime

reader = easyocr.Reader(['en'])

def analyze(img, show=False):
    # Optimizing the image

    #img = imutils.resize(img, height=500)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.Canny(img, 100, 200)
    #img = cv2.threshold(img, 110, 255, cv2.THRESH_TOZERO)[1]
    img = cv2.bilateralFilter(img,17, 33, 33)
    #img = cv2.medianBlur(img, 3)
    #img = cv2.medianBlur(img, 3)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,21, 21)
    #img = cv2.GaussianBlur(img, (1,3), 0)

    #blur   = cv2.GaussianBlur(img, (5,5), 0)
    #img = cv2.Canny(blur,1,35)
    img = img[150:250, 40:400]

    if show:
        cv2.imshow('image', img)
        cv2.waitKey(0)


    bounds = reader.readtext(img , allowlist ='0123456789', decoder='beamsearch', text_threshold=0.75, low_text=0.1)
    if bounds is not None and len(bounds) == 1:
        bound = bounds[0]
        return bound[1], bound[2]
    return (f"undecoded-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}", 0)



if __name__ == '__main__':

    os.environ['TESSDATA_PREFIX'] = 'tessdata'


    #img_file = "img.raw"
    img_file = "2398158.raw"
    img_file = "2398096.raw"
    img_file = "2398969.raw"
    image_size = (405, 720)
    img_file = 'data/002349247.jpg'
    img_file = 'data/002399250.jpg' #wrong 0 instead of 8

    print('img_file', img_file, image_size)

    if 'raw' in img_file:
        with open(img_file, 'rb') as f:
            pixels = f.read()
        img = np.frombuffer(pixels, np.uint8).reshape(image_size[1], image_size[0], 4)
    else:
        img = cv2.imread(img_file)


    string, conf = analyze(img, show=True)
    print(string, conf)

    '''
    import keras_ocr
    filename = 'savedImage.jpg'
    cv2.imwrite(filename, img)
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(filename)]
    prediction_groups = pipeline.recognize(images)
    print(prediction_groups)
    '''

    # OCR
    #ocr_result = pyt.image_to_string(img,  lang='lets', config='--psm 7 -c tessedit_char_whitelist=.0123456789')
    #print('lets', ocr_result)
    #ocr_result = pyt.image_to_string(img,  lang='letsgodigital', config='--psm 7 -c tessedit_char_whitelist=.0123456789')
    #print('digial', ocr_result)
