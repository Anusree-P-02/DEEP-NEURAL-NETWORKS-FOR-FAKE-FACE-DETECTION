import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Step 1: Load the saved model
model = tf.keras.models.load_model('fake_face_detection_model.keras')

# Step 2: Function to load and preprocess the image
def load_and_preprocess_image(img_path, target_size=(150, 150)):
    """
    Loads and preprocesses the image for prediction.
    
    Args:
        img_path (str): The path to the image file.
        target_size (tuple): The target size for resizing the image.

    Returns:
        np.array: The preprocessed image as an array ready for prediction.
    """
    img = image.load_img(img_path, target_size=target_size)  # Load the image
    img_array = image.img_to_array(img)  # Convert image to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image
    return img_array

# Step 3: Function to predict whether the image is fake or original
def detect_fake_face(model, img_path):
    """
    Predicts if the input image is fake or original using the trained model.
    
    Args:
        model (tf.keras.Model): The loaded trained model.
        img_path (str): Path to the image file to be predicted.

    Returns:
        str: The prediction result ("Fake Image" or "Original Image").
    """
    img_array = load_and_preprocess_image(img_path)
    prediction = model.predict(img_array)
    
    # Convert the prediction result to class label
    if prediction > 0.5:
        return "Original Image"
    else:
        return "Fake Image"

# Step 4: Provide the path to the new image to be classified
img_path = r"C:\fake images"  # Replace with your image path
result = detect_fake_face(model, img_path)
print(f"The input image is: {result}")
