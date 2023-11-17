""" Enter following details """

main_dir_name = "/Users/michaelbiddle/CEED_RP/pipe_bends"

""" """

import os
from PIL import Image
import PIL
import shutil

def images_are_same(image_paths):
    first_image = Image.open(image_paths[0])

    for path in image_paths[1:]:
        current_image = Image.open(path)

        if first_image.size != current_image.size:
            return False

        if first_image.tobytes() != current_image.tobytes():
            return False

    return True

similar_dir = "{}/duplicate_images".format(main_dir_name)
unique_dir = "{}/unique_images".format(main_dir_name)

os.makedirs(similar_dir, exist_ok=True)
os.makedirs(unique_dir, exist_ok=True)

photo_directory = "{}/images".format(main_dir_name)

total_img = len(os.listdir(photo_directory))

all_files = os.listdir(photo_directory)

image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

image_paths = [os.path.join(photo_directory, file) for file in image_files]

print("Deleting Unreadable Images")

count = 0

for path in image_paths:
    try:
        x = Image.open(path)
    except PIL.UnidentifiedImageError:
        os.remove(path)
        count += 1

all_files = os.listdir(photo_directory)

image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

image_paths = [os.path.join(photo_directory, file) for file in image_files]

print("Collecting Similar and Duplicate Images")

similar_images = {}

for path in image_paths:
    found_similar = False

    for key in similar_images:
        if images_are_same([path] + similar_images[key]):
            found_similar = True
            similar_images[key].append(path)
            break

    if not found_similar:
        similar_images[path] = [path]

print("Filtering Similar and Duplicate Images")

for key in similar_images:
    images = similar_images[key]
    if len(images) > 1:
        unique_image = images[0]
        destination = os.path.join(unique_dir, os.path.basename(unique_image))
        shutil.move(unique_image, destination)

        for image in images[1:]:
            destination = os.path.join(similar_dir, os.path.basename(image))
            shutil.move(image, destination)
    else:
        for image in images:
            destination = os.path.join(unique_dir, os.path.basename(image))
            shutil.move(image, destination)

print("Images filtered successfully!")

duplicates = len(os.listdir(similar_dir))
uniques = len(os.listdir(unique_dir))

print("{} Total Unfiltered Images".format(total_img))
print("{} Unreadable Images".format(count))
print("{} Duplicate Images".format(duplicates))
print("{} Unique Images".format(uniques))

shutil.rmtree(photo_directory)
os.rename(unique_dir, photo_directory)
shutil.rmtree(similar_dir)
