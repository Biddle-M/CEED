""" Enter following details """

main_dir_name = input("Enter Path to Main Directory: ")

test_images_dir = input("Enter Path to Directory With All Testing Images: ")

""" """

import os
import shutil

print("Moving best.pt Into yolov7 Directory")

file_name = "best.pt"
new_file_name = "yolov7_custom.pt"
source_directory = '{}/yolov7/runs/train/yolov7-custom/weights'.format(main_dir_name)
destination_directory = "{}/yolov7".format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

count = 0

for root, dirs, files in os.walk("{}".format(test_images_dir)):
    for file in files:
        count += 1
        source_path = os.path.join(root, file)
        destination_path = os.path.join("{}/yolov7".format(main_dir_name), "{}.jpg".format(count))
        shutil.move(source_path, destination_path)

shutil.rmtree('{}'.format(test_images_dir))

import subprocess

for num in range(1, count + 1):
    subprocess.run(["python3", "{}/yolov7/detect.py".format(main_dir_name), "--weights", "yolov7_custom.pt", "--conf", "0.5", "--img-size", "640", "--source", "{}.jpg".format(num), "--no-trace"])
    os.remove('{}/yolov7/{}.jpg'.format(main_dir_name, num))

os.makedirs('{}/Testing_Results'.format(main_dir_name))

file_name = "1.jpg"
new_file_name = "test_1.jpg"
source_directory = '{}/yolov7/runs/detect/exp'.format(main_dir_name)
destination_directory = "{}/Testing_Results".format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

for num in range(2, count + 1):
    file_name = "{}.jpg".format(num)
    new_file_name = "test_{}.jpg".format(num)
    source_directory = '{}/yolov7/runs/detect/exp{}'.format(main_dir_name, num)
    destination_directory = "{}/Testing_Results".format(main_dir_name)
    source_path = os.path.join(source_directory, file_name)
    destination_path = os.path.join(destination_directory, new_file_name)
    shutil.move(source_path, destination_path)

shutil.rmtree('{}/yolov7/runs/detect'.format(main_dir_name))
