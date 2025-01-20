import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model
model = tf.keras.models.load_model(r'C:\New Dataset\fake_face_detection_model.keras')  # Update the path

# Function to load and preprocess the image
def load_and_preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict the result
def detect_fake_face(model, img_path):
    img_array = load_and_preprocess_image(img_path)
    prediction = model.predict(img_array)
    return "Original Image" if prediction > 0.5 else "Fake Image"

# Function to open an image and display the result
def open_image():
    img_path = filedialog.askopenfilename()  # Ask user to select an image file
    if img_path:
        # Display the image in the GUI
        img = Image.open(img_path)
        img = img.resize((200, 200))  # Resize the image for display
        img_tk = ImageTk.PhotoImage(img)
        panel.configure(image=img_tk)
        panel.image = img_tk

        # Run the detection and show the result
        result = detect_fake_face(model, img_path)
        result_label.config(text=f"Result: {result}")

# Create the GUI window
root = tk.Tk()
root.title("Fake Face Detection")

# Add a label for the result
result_label = Label(root, text="Result: ", font=('Arial', 18))
result_label.pack(pady=10)

# Add an image display panel
panel = Label(root)
panel.pack()

# Add a button to load an image
load_btn = tk.Button(root, text="Load Image", command=open_image, font=('Arial', 14))
load_btn.pack(pady=20)

# Start the GUI loop
root.mainloop()
