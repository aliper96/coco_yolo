import os
import numpy as np
import random
import glob
import shutil
from  tqdm import tqdm

train_images = "dataset/train/images/"
train_labels = "dataset/train/labels/"
val_images = "dataset/val/images/"
val_labels = "dataset/val/labels/"

paths = [train_images,train_labels,val_images,val_labels]

for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)

images =  glob.glob("images/*.png")
random.shuffle(images)
train = images[:int(0.8 * len(images))]
test = images[int(0.8 * len(images)):]

for i in tqdm(train):
    name = i.split("\\")[1][:-4]
    shutil.copyfile("images/"+ name+ ".png", train_images+ name+".png")
    shutil.copyfile("yolotxt/"+ name + ".txt", train_labels +name+ ".txt")

for i in tqdm(test):
    name = i.split("\\")[1][:-4]
    shutil.copyfile("images/"+ name+ ".png", val_images + name+ ".png" )
    shutil.copyfile("yolotxt/"+ name + ".txt", val_labels + name+ ".txt")

print("ended")

