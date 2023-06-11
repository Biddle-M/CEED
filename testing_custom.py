""" Enter following details """

main_dir_name = "/home/mbiddle"

training_results_dir = "/scratch/pmc013/mbiddle/CEED"

batch_number = '93615'

test_images_dir = "/group/pmc013/mbiddle/test_images"

""" """

import os
import shutil

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

for num in range(1, count + 1):
    subprocess.run(["python", "{}/yolov7/detect.py".format(main_dir_name), "--weights", '{}/{}/runs/train/yolov7-custom/weights/best.pt'.format(training_results_dir, batch_number), "--conf", "0.5", "--img-size", "640", "--source", "{}.jpg".format(num), "--no-trace"])
    os.remove('{}/yolov7/{}.jpg'.format(main_dir_name, num))

os.makedirs('{}/test_results'.format(main_dir_name))

for num in range(1, count + 1):
    if num == 1:
        source_directory = '{}/yolov7/runs/detect/exp'.format(main_dir_name)
    else:
        source_directory = '{}/yolov7/runs/detect/exp{}'.format(main_dir_name, num)
    destination_directory = "{}/test_results".format(main_dir_name)
    source_path = os.path.join(source_directory, "{}.jpg".format(num))
    destination_path = os.path.join(destination_directory, "test_{}.jpg".format(num))
    shutil.move(source_path, destination_path)

shutil.rmtree('{}/yolov7/runs'.format(main_dir_name))
