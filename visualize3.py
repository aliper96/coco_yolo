import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

json_path = "0205221008__135.txt"
image_path =  "0205221008__135.jpeg"
window_name = 'Image'
dim = (500, 500)
#RGB-BGR
blue_color = (255,144,30)
red_color = (0, 0, 255)

def mouseRGB(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        print("Coordinates of pixel: X: ",x,"Y: ",y)

cv.namedWindow('mouseRGB')
cv.setMouseCallback('mouseRGB',mouseRGB)



with open(json_path, 'r', encoding='UTF-8') as file:
    img_color = cv.imread(image_path, 1)
    img_color = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)

    print(img_color.shape)
    # r = cv.selectROI(img_color)
    # print("roy ", r)

    lines = file.readlines()
    for line in lines:
        line = line.split(" ")[1:]


        img_width = img_color.shape[0]
        img_height = img_color.shape[1]




        x_tl = float(line[0])
        y_tl = float(line[1])
        w = float(line[2])
        h = float(line[3].split("\n")[0])

        # x = (xmin ) * dw / 2

        width_coco = w * img_width
        height_coco = h * img_height
        x_coco = x_tl * img_width - (width_coco/2)
        y_coco = y_tl * img_height - (height_coco/2)
        # img_color = cv.rectangle(img_color, (24, 187), (158, 416), red_color, 2)
        x = int (x_coco)
        y = int (y_coco)
        w = int (width_coco)
        h = int (height_coco)


        print(x,y,w,h)
        img_color = cv.rectangle(img_color, (x, y), (w+x, h+y), red_color, 2)


    cv.imshow("mouseRGB", img_color)

    k = cv.waitKey(0)