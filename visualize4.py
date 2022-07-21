import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import glob
from  tqdm import tqdm


json_path = "0205221008__135.txt"
image_path =  "0205221008__135.jpeg"
window_name = 'Image'


img_real_folder_path =  "yolo_dataset_validation/images/val/"
text_folder_path =  "yolo_dataset_validation/labels/val/"
images_folder_path = "exp4/"
output_folder_path = "output_validate/"
ext_img = ".jpg"
ext_img_2 = ".jpeg"

dim = (624, 624)
#RGB-BGR
blue_color = (255,144,30)
red_color = (0, 25, 255)

def mouseRGB(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        print("Coordinates of pixel: X: ",x,"Y: ",y)

# cv.namedWindow('mouseRGB')
# cv.setMouseCallback('mouseRGB',mouseRGB)

list_annotation = glob.glob(text_folder_path + './*.txt')

for annotation in tqdm(list_annotation):
    is_annotated = False
    filename = annotation.split("\\")[-1][:-4]

    with open(text_folder_path + filename + ".txt", 'r', encoding='UTF-8') as file:
        img_color = cv.imread(img_real_folder_path + filename + ext_img, 1)
        img_color_pre = cv.imread(images_folder_path + filename + ext_img_2, 1)

        if img_color is None:
            continue
        if img_color_pre is None:
            continue

        img_color_pre = cv.resize(img_color_pre, dim, interpolation=cv.INTER_AREA)
        img_color = cv.resize(img_color, dim, interpolation=cv.INTER_AREA)
        img_color_annotated = img_color.copy()

        # print(img_color.shape)

        lines = file.readlines()
        for line in lines:
            line = line.split(" ")[1:]


            img_width = img_color_annotated.shape[0]
            img_height = img_color_annotated.shape[1]

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

            is_annotated = True
            # print(x,y,w,h)
            img_color_annotated = cv.rectangle(img_color_annotated, (x, y), (w+x, h+y), red_color, 2)

    img_color = cv.copyMakeBorder(img_color, 5, 5, 5, 5, cv.BORDER_CONSTANT, value=[0,0,0])
    img_color_annotated = cv.copyMakeBorder(img_color_annotated, 5, 5, 5, 5, cv.BORDER_CONSTANT, value=[0,0,0])
    img_color_pre = cv.copyMakeBorder(img_color_pre, 5, 5, 5, 5, cv.BORDER_CONSTANT, value=[0,0,0])

    vis = np.concatenate((img_color, img_color_annotated, img_color_pre), axis=1)

    if is_annotated:
        filename += "_anted"
    # cv.imshow("mouseRGB", img_color)
    cv.imwrite(output_folder_path + filename + ".png", vis)

        # k = cv.waitKey(0)