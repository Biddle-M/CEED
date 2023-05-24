""" Enter following details """

main_dir_name = "/home/vagrant/jack_sparrow"

images_dir = "images"

labels_dir = "labels"

proportion_train_images = 0.9

workers = "1"
batchsize = "8"
epochs = "100"
img1 = "640"
img2 = "640"

import os
import shutil

print("Creating Destination Folders")

os.makedirs('{}/yolov7-main/data/train'.format(main_dir_name))
os.makedirs('{}/yolov7-main/data/val'.format(main_dir_name))

destination_folder_ti = '{}/yolov7-main/data/train/images'.format(main_dir_name)
destination_folder_tl = '{}/yolov7-main/data/train/labels'.format(main_dir_name)
destination_folder_vi = '{}/yolov7-main/data/val/images'.format(main_dir_name)
destination_folder_vl = '{}/yolov7-main/data/val/labels'.format(main_dir_name)
os.makedirs(destination_folder_ti)
os.makedirs(destination_folder_tl)
os.makedirs(destination_folder_vi)
os.makedirs(destination_folder_vl)

import os
import shutil

source_directory = '{}/{}'.format(main_dir_name, images_dir)
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

source_directory2 = '{}/{}'.format(main_dir_name, labels_dir)
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

shutil.rmtree('{}/{}'.format(main_dir_name, images_dir))
shutil.rmtree('{}/{}'.format(main_dir_name, labels_dir))

print("Training Begins")

import subprocess

subprocess.run(["python", "{}/yolov7-main/train.py".format(main_dir_name), "--workers", workers, "--batch-size", batchsize, "--epochs", epochs, "--img", img1, img2, "--data", "data/custom_data.yaml", "--hyp", "data/hyp.scratch.custom.yaml", "--cfg", "cfg/training/yolov7-custom.yaml", "--name", "yolov7-custom", "--weights", "yolov7.pt"])