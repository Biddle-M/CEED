""" Enter following details """

main_dir_name = "/Users/michaelbiddle/CEED_RP/jack_sparrow"

test_images_dir = "test_images"


import os
import shutil

print("Moving best.pt Into yolov7-main Directory")

file_name = "best.pt"
new_file_name = "yolov7_custom.pt"
source_directory = '{}/yolov7-main/runs/train/yolov7-custom/weights'.format(main_dir_name)
destination_directory = "{}/yolov7-main".format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

count = 0

for root, dirs, files in os.walk("{}/{}".format(main_dir_name, test_images_dir)):
    for file in files:
        count += 1
        source_path = os.path.join(root, file)
        destination_path = os.path.join("{}/yolov7-main".format(main_dir_name), "{}.jpg".format(count))
        shutil.move(source_path, destination_path)

shutil.rmtree('{}/{}'.format(main_dir_name, test_images_dir))

import subprocess

for num in range(1, count + 1):
    subprocess.run(["python3", "{}/yolov7-main/detect.py".format(main_dir_name), "--weights", "yolov7_custom.pt", "--conf", "0.5", "--img-size", "640", "--source", "{}.jpg".format(num), "--no-trace"])
    os.remove('{}/yolov7-main/{}.jpg'.format(main_dir_name, num))

os.makedirs('{}/Testing_Results'.format(main_dir_name))

file_name = "1.jpg"
new_file_name = "test_1.jpg"
source_directory = '{}/yolov7-main/runs/detect/exp'.format(main_dir_name)
destination_directory = "{}/Testing_Results".format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

for num in range(2, count + 1):
    file_name = "{}.jpg".format(num)
    new_file_name = "test_{}.jpg".format(num)
    source_directory = '{}/yolov7-main/runs/detect/exp{}'.format(main_dir_name, num)
    destination_directory = "{}/Testing_Results".format(main_dir_name)
    source_path = os.path.join(source_directory, file_name)
    destination_path = os.path.join(destination_directory, new_file_name)
    shutil.move(source_path, destination_path)

shutil.rmtree('{}/yolov7-main/runs/detect'.format(main_dir_name))