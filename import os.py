import os
from PIL import Image
import hashlib

# Directory containing the images
dataset_dir = r"C:\New Dataset\Images"

# Supported image formats
supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

def is_image_valid(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Check if the image is corrupted
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

# Remove corrupted images
remove_corrupted_images(dataset_dir)

# Find and remove duplicate images
duplicates = find_duplicate_images(dataset_dir)
if duplicates:
    remove_duplicates(duplicates)
else:
    print("No duplicates found.")

print("Dataset cleaning complete.")

from tensorflow.keras.callbacks import ModelCheckpoint

# Define model checkpoint callback
checkpoint = ModelCheckpoint(filepath='best_model.keras', monitor='val_loss', save_best_only=True)

# Add the checkpoint callback to the model's fit method
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    callbacks=[checkpoint]
)
