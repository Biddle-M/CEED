""" Enter following details """

main_dir_name = input("Enter Path to Main Directory: ")

num_of_classes = int(input("Enter Number of Labelled Classes: "))

name_of_classes = []

for num in range(num_of_classes):
    new_class = input("Class {}: ".format(num + 1))
    name_of_classes.append(new_class)

print("Editing custom_data.yaml File with {} Classes of Names {}".format(num_of_classes, name_of_classes))

file_path = '{}/yolov7-main/data/custom_data.yaml'.format(main_dir_name)
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

file_path2 = '{}/yolov7-main/cfg/training/yolov7-custom.yaml'.format(main_dir_name)
line_numbers2 = [2]
new_lines2 = ['nc: {}'.format(num_of_classes)]

with open(file_path2, 'r') as file2:
    lines2 = file2.readlines()

for i2, line_number2 in enumerate(line_numbers2):
    if line_number2 <= len(lines2):
        lines2[line_number2 - 1] = new_lines2[i2] + '\n'

with open(file_path2, 'w') as file2:
    file2.writelines(lines2)
