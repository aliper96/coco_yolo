import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

json_path = "0205221008__135.json"
image_path =  "0205221008__135.jpeg"
window_name = 'Image'
dim = (640, 640)
#RGB-BGR
blue_color = (255,144,30)
red_color = (0, 0, 255)


black_image = np.ones(shape=(512,512,3), dtype=np.int16)
with open(json_path, 'r+') as f:
  data = json.load(f)
  img_color = cv.imread(image_path, 1)
  rec_list = data["annotations"]
  for annotation in rec_list:
    rec = annotation["bounding_box"]
    _x=int(rec['x'])
    _y=int(rec['y'])
    _h=int(rec['h'])
    _w=int(rec['w'])
    img_color = cv.rectangle(img_color, (_x, _y), (_x + _w, _y + _h), blue_color, 2)


    poli = annotation['polygon']["path"]

    list_poli = np.array([(x['x'],x['y']) for x in poli],np.int32)
    pts = list_poli.reshape((-1, 1, 2))
    img_color = cv.polylines(img_color, [pts], True, blue_color)
    x, y, w, h = cv.boundingRect(pts)

    img_color = cv.rectangle(img_color, (x, y), (x + w, y + h), red_color, 2)
    print("OPENCV :" , x,y,w,h)
    print("YOLO :" , _x, _y, _w, _h)

  resized = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)


  cv.imshow("Display window", resized)

  k = cv.waitKey(0)