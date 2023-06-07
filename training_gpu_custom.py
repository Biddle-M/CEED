""" Enter following details """

main_dir_name = "/home/mbiddle"

num_of_classes = 1

name_of_classes = ["Jack Sparrow"]

images_dir = "/group/pmc013/mbiddle/images"

labels_dir = "/group/pmc013/mbiddle/labels"

proportion_train_images = 0.9

workers = "1"
device = "0"
batchsize = "8"
epochs = "100"
img1 = "640"
img2 = "640"

""" """

print("Editing custom_data.yaml File with {} Classes of Names {}".format(num_of_classes, name_of_classes))

file_path = '{}/yolov7/data/custom_data.yaml'.format(main_dir_name)
line_numbers = [5, 8]
new_lines = ['nc: {}'.format(num_of_classes), 'names: {}'.format(name_of_classes)]

with open(file_path, 'r') as file:
    lines = file.readlines()

for i, line_number in enumerate(line_numbers):
    if line_number <= len(lines):
        lines[line_number - 1] = new_lines[i] + '\n'

with open(file_path, 'w') as file:
    file.writelines(lines)

print("Editing yolov7-custom.yaml File with {} Classes".format(num_of_classes))

file_path2 = '{}/yolov7/cfg/training/yolov7-custom.yaml'.format(main_dir_name)
line_numbers2 = [2]
new_lines2 = ['nc: {}'.format(num_of_classes)]

with open(file_path2, 'r') as file2:
    lines2 = file2.readlines()

for i2, line_number2 in enumerate(line_numbers2):
    if line_number2 <= len(lines2):
        lines2[line_number2 - 1] = new_lines2[i2] + '\n'

with open(file_path2, 'w') as file2:
    file2.writelines(lines2)

import os
import shutil

print("Creating Destination Folders")

os.makedirs('{}/yolov7/data/train'.format(main_dir_name))
os.makedirs('{}/yolov7/data/val'.format(main_dir_name))

destination_folder_ti = '{}/yolov7/data/train/images'.format(main_dir_name)
destination_folder_tl = '{}/yolov7/data/train/labels'.format(main_dir_name)
destination_folder_vi = '{}/yolov7/data/val/images'.format(main_dir_name)
destination_folder_vl = '{}/yolov7/data/val/labels'.format(main_dir_name)
os.makedirs(destination_folder_ti)
os.makedirs(destination_folder_tl)
os.makedirs(destination_folder_vi)
os.makedirs(destination_folder_vl)

import os
import shutil

source_directory = '{}'.format(images_dir)
destination_directory_1 = destination_folder_ti
destination_directory_2 = destination_folder_vi

files = os.listdir(source_directory)
files.sort()

num_files_to_move = round(len(files) * proportion_train_images)

for file in files[:num_files_to_move]:
    if not file.startswith('.DS_Store'):
        source_path = os.path.join(source_directory, file)
        destination_path = os.path.join(destination_directory_1, file)
        shutil.move(source_path, destination_path)
    
for file in files[num_files_to_move:]:
    if not file.startswith('.DS_Store'):
        source_path = os.path.join(source_directory, file)
        destination_path = os.path.join(destination_directory_2, file)
        shutil.move(source_path, destination_path)

source_directory2 = '{}'.format(labels_dir)
destination_directory_3 = destination_folder_tl
destination_directory_4 = destination_folder_vl

files2 = os.listdir(source_directory2)
files2.sort()

for file in files2[:num_files_to_move]:
    if not file.startswith('.DS_Store'):
        source_path = os.path.join(source_directory2, file)
        destination_path = os.path.join(destination_directory_3, file)
        shutil.move(source_path, destination_path)
    
for file in files2[num_files_to_move:]:
    if not file.startswith('.DS_Store'):
        source_path = os.path.join(source_directory2, file)
        destination_path = os.path.join(destination_directory_4, file)
        shutil.move(source_path, destination_path)

shutil.rmtree('{}'.format(images_dir))
shutil.rmtree('{}'.format(labels_dir))

print("Training Begins")

import subprocess

subprocess.run(["python", "{}/yolov7/train.py".format(main_dir_name), "--workers", workers, "--device", device, "--batch-size", batchsize, "--epochs", epochs, "--img", img1, img2, "--data", "data/custom_data.yaml", "--hyp", "data/hyp.scratch.custom.yaml", "--cfg", "cfg/training/yolov7-custom.yaml", "--name", "yolov7-custom", "--weights", "yolov7.pt"])
