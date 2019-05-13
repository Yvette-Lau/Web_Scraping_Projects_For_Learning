# encoding:  utf-8


import os

images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
print(images_path)
if not os.path.exists(images_path):
    print("File not exists...")
    os.mkdir(images_path)

else:
    print("File is here!!!")