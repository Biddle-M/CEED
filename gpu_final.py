""" """

print('Extracting variables from input_details.txt')

text_file = 'input_details.txt'

with open(text_file, 'r') as file:
    content = file.readlines()

variables = {}
for line in content:
    key, value = line.strip().split('=')
    if ',' in value:
        value = value.split(',')
    variables[key] = value

main_dir_name = variables['main_dir_name']
num_of_classes = int(variables['num_of_classes'])
name_of_classes = variables['name_of_classes']
images_dir = variables['images_dir']
labels_dir = variables['labels_dir']
training_results_dir = variables['training_results_dir']
batch_number = int(variables['batch_number'])
test_images_dir = variables['test_images_dir']
proportion_train_images = int(variables['proportion_train_images'])
workers = variables['workers']
device = variables['device']
batchsize = variables['batchsize']
epochs = variables['epochs']
img1 = variables['img1']
img2 = variables['img2']

""" """

print'Editing custom_data.yaml File with {} Classes of Names {}'.format(num_of_classes, name_of_classes))

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

print('Editing yolov7-custom.yaml File with {} Classes'.format(num_of_classes))

file_path2 = '{}/yolov7/cfg/training/yolov7.yaml'.format(main_dir_name)
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

print('Training Begins')

import subprocess

subprocess.run(['python', '{}/yolov7/train.py'.format(main_dir_name), '--workers', workers, '--device', device, '--batch-size', batchsize, '--epochs', epochs, '--img', img1, img2, '--data', '{}/yolov7/data/custom_data.yaml'.format(main_dir_name), '--hyp', '{}/yolov7/data/hyp.scratch.custom.yaml'.format(main_dir_name), '--cfg', '{}/yolov7/cfg/training/yolov7.yaml'.format(main_dir_name), '--name', 'yolov7-custom', '--weights', '{}/yolov7/yolov7.pt'.format(main_dir_name)])

print('Training Completed')

shutil.rmtree('{}/yolov7/data/train'.format(main_dir_name))
shutil.rmtree('{}/yolov7/data/val'.format(main_dir_name))

print('Moving best.pt Into yolov7 Directory')

file_name = 'best.pt'
new_file_name = 'yolov7_custom.pt'
source_directory = '{}/{}/runs/train/yolov7-custom/weights'.format(training_results_dir, batch_number)
destination_directory = '{}/yolov7'.format(main_dir_name)
source_path = os.path.join(source_directory, file_name)
destination_path = os.path.join(destination_directory, new_file_name)
shutil.move(source_path, destination_path)

count = 0

for root, dirs, files in os.walk("{}".format(test_images_dir)):
    for file in files:
        if not file.startswith('.DS_Store'):
            count += 1
            source_path = os.path.join(root, file)
            destination_path = os.path.join('{}/yolov7'.format(main_dir_name), '{}.jpg'.format(count))
            shutil.move(source_path, destination_path)

shutil.rmtree('{}'.format(test_images_dir))

import subprocess

print('Detection Begins')

for num in range(1, count + 1):
    subprocess.run(['python', '{}/yolov7/detect.py'.format(main_dir_name), '--weights', '{}/yolov7/yolov7_custom.pt'.format(main_dir_name), '--conf', '0.5', '--img-size', '640', '--source', '{}/yolov7/{}.jpg'.format(main_dir_name, num), '--no-trace'])
    os.remove('{}/yolov7/{}.jpg'.format(main_dir_name, num))

print('Detection Completed')