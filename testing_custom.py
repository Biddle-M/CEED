""" Enter following details """

main_dir_name = "/home/mbiddle"

training_results_dir = "/scratch/pmc013/mbiddle/CEED"

batch_number = 'pipe_bends2'

test_images_dir = "/group/pmc013/mbiddle/test_images"

""" """

import os
import shutil

print("Moving best.pt Into yolov7 Directory")

file_name = "best.pt"
new_file_name = "yolov7_custom.pt"
source_directory = '{}/{}/runs/train/yolov7-custom/weights'.format(training_results_dir, batch_number)
destination_directory = "{}/yolov7".format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

count = 0

for root, dirs, files in os.walk("{}".format(test_images_dir)):
    for file in files:
        if not file.startswith('.DS_Store'):
            count += 1
            source_path = os.path.join(root, file)
            destination_path = os.path.join("{}/yolov7".format(main_dir_name), "{}.jpg".format(count))
            shutil.move(source_path, destination_path)

shutil.rmtree('{}'.format(test_images_dir))

import subprocess

print("Detection Begins")

for num in range(1, count + 1):
    subprocess.run(["python", "{}/yolov7/detect.py".format(main_dir_name), "--weights", "{}/yolov7/yolov7_custom.pt".format(main_dir_name), "--conf", "0.5", "--img-size", "640", "--save-txt", "--source", "{}/yolov7/{}.jpg".format(main_dir_name, num), "--no-trace"])
    os.remove('{}/yolov7/{}.jpg'.format(main_dir_name, num))

print("Detection Completed")