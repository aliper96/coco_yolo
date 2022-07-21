import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import  os
import  glob
from  tqdm import tqdm

crop_black = False  # not working yet
just_val = True
just_train = False
create_empty_json = True
window_name = 'Image'
resize = True
dim = (608,608)
#RGB-BGR
blue_color = (255,144,30)
red_color = (0, 0, 255)
names= np.array(['Alternaria', 'Basidiospora', 'Cladosporium', 'HDE'])

img_folder_path = "validation_data/Pattern_Pollen_Detector/"
img_ext = ".jpeg"
json_folder_path = "validation_data/patternhde0.1/annotations/"

yolo_folder = "yolo_dataset_validdation/"
yolo_label_train = "labels/train/"
yolo_label_val = "labels/val/"
yolo_images_train = "images/train/"
yolo_images_val = "images/val/"

if not os.path.exists(yolo_folder+yolo_label_train):
  os.makedirs(yolo_folder+yolo_label_train)
if not os.path.exists(yolo_folder+yolo_label_val):
  os.makedirs(yolo_folder+yolo_label_val)
if not os.path.exists(yolo_folder+yolo_images_train):
  os.makedirs(yolo_folder+yolo_images_train)
if not os.path.exists(yolo_folder+yolo_images_val):
  os.makedirs(yolo_folder+yolo_images_val)


list_jsons = glob.glob(json_folder_path+ './*.json')


def crop(image):
  y_nonzero, x_nonzero, _ = np.nonzero(image)
  return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

for i, json_path in enumerate(tqdm(list_jsons)):
  filename = json_path.split("\\")[-1][:-5]
  # if filename == "2812211634_0_2.360_10.636_-0.072":
  #   print("adsfa")
  with open(json_path, 'r+') as f:
    data = json.load(f)
    img_color = cv.imread(img_folder_path + filename + img_ext, 1)
    if img_color is None:
      f.close()
      os.remove(f.name)
      continue
    rec_list = data["annotations"]
    yolo_annotation = []
    for annotation in rec_list:
      try:
        poli = annotation['polygon']["path"]
      except:
        continue

      list_poli = np.array([(x['x'],x['y']) for x in poli],np.int32)
      pts = list_poli.reshape((-1, 1, 2))
      # img_color = cv.polylines(img_color, [pts], True, blue_color)
      x, y, w, h = cv.boundingRect(pts)
      # img_color = cv.rectangle(img_color, (x, y), (x + w, y + h), red_color, 2)
      img_height, img_width , _ = img_color.shape


      with_yolo = (w) / img_width
      height_yolo = (h) / img_height
      x_yolo = x  / img_width +  (with_yolo/2)
      y_yolo =  y / img_height + (height_yolo/2)

      # print("OPENCV :" , x,y,w,h)
      id = np.where(names == annotation["name"])
      if not np.any(names == annotation["name"]):
        continue
      yolo_annotation.append([id[0],x_yolo,y_yolo,with_yolo,height_yolo])

    if not create_empty_json:
      if not np.any(yolo_annotation):
        continue
    if just_val:
    # if (i % 7 == 0):
      with open(yolo_folder+yolo_label_val+filename+".txt", 'w') as f:
        if crop_black:
          img_color = crop(img_color)
        if resize:
          img_color = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)
        cv.imwrite(yolo_folder + yolo_images_val + filename + '.jpg', img_color)
        for item in yolo_annotation:
          try:
            f.write("%i %f %f %f %f\n" % (item[0], item[1],item[2], item[3], item[4]))
          except:
            continue
    if just_train:
    # if(i % 7 != 0) :

      with open(yolo_folder + yolo_label_train + filename + ".txt", 'w') as f:
        if crop_black:
          img_color = crop(img_color)
        if resize:
          img_color = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)

        cv.imwrite(yolo_folder + yolo_images_train + filename + '.jpg', img_color)
        for item in yolo_annotation:
          # write each item on a new line
          try:
            f.write("%i %f %f %f %f\n" % (item[0], item[1], item[2], item[3], item[4]))
          except:
            continue

  # resized = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)


  # cv.imshow("Display window", resized)

  # k = cv.waitKey(0)