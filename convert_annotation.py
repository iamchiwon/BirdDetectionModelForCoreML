import os
import random
import json
from shutil import copyfile
from PIL import Image

label_dir = "./archive/labels"
image_dir = "./archive/images"

def convert_format(filename, image_path):
    image = Image.open(f"{image_path}/{filename}.jpg")
    i_width, i_height = image.size

    with open(f"{label_dir}/{filename}.txt", mode='r') as f:
        line = f.readline().split(" ")

        # YOLO format
        class_id = line[0]
        x_center = float(line[1])
        y_center = float(line[2])
        width = float(line[3])
        height = float(line[4])

        # Convert
        to_x = int((x_center - width / 2) * i_width)
        to_y = int((y_center - height / 2) * i_height)
        to_w = int(width * i_width)
        to_h = int(height * i_height)

        return {
            "image": f"{filename}.jpg",
            "annotations": [{
                "label": "bird",
                "coordinates": {
                    "x": to_x,
                    "y": to_y,
                    "width": to_w,
                    "height": to_h
                }
            }]
        }

def convert_formats(src, target):
    anotation_data = []

    # Remove old files
    if os.path.exists(f"./{target}"):
        for f in os.listdir(f"./{target}"):
            os.remove(f"./{target}/{f}")
    os.makedirs(f"./{target}", exist_ok=True)

    for s in src:
        filename = s.split(".")[0]
        # copy image file to target
        copyfile(f"{image_dir}/{filename}.jpg", f"./{target}/{filename}.jpg")
        data = convert_format(filename, image_dir)
        anotation_data.append(data)

    # write annotation.json to target directory
    with open(f"./{target}/annotation.json", mode='w') as f:
        json.dump(anotation_data, f)


all_labels = os.listdir(label_dir)
random.shuffle(all_labels)

convert_formats(all_labels[:1500], "train")
convert_formats(all_labels[1500:], "test")

