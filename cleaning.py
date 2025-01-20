import os
from PIL import Image
import hashlib

# Dataset directory
dataset_dir = r"C:\New Dataset\Images"
categories = ['fake_image', 'original_image']

# Supported image formats
supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

def is_image_valid(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError) as e:
        print(f"Corrupted image detected: {image_path}")
        return False

def remove_corrupted_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file)[1].lower() in supported_formats:
                if not is_image_valid(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")

def find_duplicate_images(directory):
    hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file)[1].lower() in supported_formats:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in hashes:
                    duplicates.append(file_path)
                else:
                    hashes[file_hash] = file_path

    return duplicates

def remove_duplicates(duplicates):
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Removed duplicate: {duplicate}")

for category in categories:
    category_dir = os.path.join(dataset_dir, category)
    remove_corrupted_images(category_dir)
    duplicates = find_duplicate_images(category_dir)
    if duplicates:
        remove_duplicates(duplicates)
    else:
        print(f"No duplicates found in {category}.")

print("Dataset cleaning complete.")
