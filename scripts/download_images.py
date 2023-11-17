""" Enter following details """

main_dir_name = "/Users/michaelbiddle/CEED_RP/pipe_bends"

keywords = ["pipe bend", "pipes service room", "water pipe bend", "drainage pipe bend", "service pipe bend", "plant room boiler pipes", "ceiling void pipes"]

num_of_images = 500

""" """

print("Generating {} Images Per Keyword From Google".format(num_of_images))

from simple_image_download import simple_image_download as simp

response = simp.simple_image_download

for kw in keywords:
    print("Generating Images for Keyword: {}".format(kw))
    response().download(kw, num_of_images)

print("Image Collection Completed")

import os
import shutil

destination_folder = '{}/images'.format(main_dir_name)
os.makedirs(destination_folder)
os.makedirs('{}/labels'.format(main_dir_name))

source_folders = []
for name in keywords:
     print("Moving {} to New Images Directory".format(name))
     path = '{}/simple_images/{}'.format(main_dir_name, name)
     source_folders.append(path)

for folder in source_folders:
    for root, dirs, files in os.walk(folder):
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                shutil.move(source_path, destination_path)

print("File Merge Completed")

shutil.rmtree('{}/simple_images'.format(main_dir_name))
