import cv2
from glob import glob
import os
from random import randrange


filename_list = glob(os.path.join("../Documents/digits/", "*.png"))
imgs = [cv2.imread(img_file) for img_file in sorted(filename_list)]

def generate():
    final = None
    label = ''
    for _ in range(9):
        idx = randrange(10)
        img = imgs[idx]
        label += str(idx)
        if final is None:
            final = img
        else:
            final = cv2.hconcat([final, img])
    return final, label

gt = ''

for i in range(50000):
    img , label = generate()
    if i % 100 == 0:
        print(i, label)
    gt += f'data/{label}.png {label}\n'
    fn = f'gen/data/{label}.png'
    cv2.imwrite(fn, img)
    #cv2.imshow('image', img)
    #cv2.waitKey(0)

with open('gen/gt.txt', 'w') as f:
    f.write(gt)

