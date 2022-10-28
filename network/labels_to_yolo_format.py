import pandas as pd
import os


# create labels folder if not exists
if os.path.exists("labels") is False:
    os.mkdir("labels")

df = pd.read_csv("HAM10000_metadata.tab")

print(df.head())

# yolo expects data labeled from 0
# txt labels class x_center y_center width height, normalized xywh format (from 0 - 1)
# one txt for each file

class_dict = {
    "nv": 0,
    "mel": 1,
    "bkl": 2,
    "bcc": 3,
    "akiec": 4,
    "vasc": 5,
    "df": 6
}

for index, row in df.iterrows():
    print(row['image_id'], row['dx'])
    name = "labels/" + row['image_id'] + ".txt"
    label = row['dx']
    with open(name, "w") as f:
        f.write("{} 0.5 0.5 1 1".format(class_dict[label]))
