import os
from tqdm import tqdm
import json

# Get the list of all files and directories
path = "annotations/"

valid_tag =['HDE','Cladosporium','Alternaria','Basidiospora']
HDE = "12"


import glob
import os
for filename in tqdm(glob.glob(path + '*.json')):
    # print(filename)
    # if filename == "annotations\\1005221154_0_37.0679_-5.0614_7.7875.json":
    #     print ("Hola")
    annonations = []

    text = []
    final_text = []
    with open(os.path.join(os.getcwd(), filename), 'r+') as f:
        data = json.load(f)
        for i, annonation in enumerate (data['annotations']):
            if annonation['name'] in valid_tag:
                # annonation['name'] = 'HDE'
                annonations.append(annonation)
        data['annotations'] = annonations
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=1)
        f.truncate()     # remove remaining part





        