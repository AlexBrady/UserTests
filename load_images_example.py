import base64
import json

with open('./pics.json', 'rb') as pics_file:
    pics = json.load(pics_file)

for pic in pics:
    with open(pic['image_path'], "rb") as image_file:
        pic['image'] = base64.b64encode(image_file.read())
    del pic['image_path']
    print(pic["image"])