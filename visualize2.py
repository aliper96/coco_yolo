import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

json_path = "0205221008__135_v2.txt"
image_path =  "0205221008__135_v2.jpg"
window_name = 'Image'
dim = (400, 416)
#RGB-BGR
blue_color = (255,144,30)
red_color = (0, 0, 255)


black_image = np.ones(shape=(512,512,3), dtype=np.int16)
with open(json_path, 'r', encoding='UTF-8') as file:
  img_color = cv.imread(image_path, 1)
  img_color = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)

  lines = file.readlines()
  for line in lines:
    line = line.split(" ")[1:]
    line = [float(l)  for l in line]
    lis = np.array([(i* dim[0],k*dim[1]) for i, k in zip(line[0::2] , line[1::2])],np.int32)
    pts = lis.reshape((-1, 1, 2))
    img_color = cv.polylines(img_color, [pts], True, blue_color)

  cv.imshow("Display window", img_color)

  k = cv.waitKey(0)
