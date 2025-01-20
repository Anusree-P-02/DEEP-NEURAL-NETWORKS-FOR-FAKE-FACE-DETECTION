from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename

hashed_password = generate_password_hash('password123')


app = Flask(__name__)  # Correct variable __name__

app.secret_key = '3d6f45a5fc12445dbac2f59c3b6c7cb1'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Update with your MySQL username
app.config['MYSQL_PASSWORD'] = 'root'  # Update with your MySQL password
app.config['MYSQL_DB'] = 'Face_Recognition'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connect to MySQL and check if the user exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):  # user[2] is the hashed password
            session['logged_in'] = True
            session['username'] = username
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cursor.fetchone()
        
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username,email, password) VALUES (%s,%s, %s)", (username,email, hashed_password))
        mysql.connection.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reg.html')

@app.route('/home')
def home():
    return render_template('index.html', result=None, image_path=None)

# Route for the logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('login_time', None)  # Optional: Clear the login time from the session
    return redirect(url_for('login'))

# @app.route('/<filename>')
# def uploaded_file(filename):
#     print(os.path.exists('uploads/short.jpg'))
#     return send_from_directory('uploads', filename)


model_path = r"fake_face_detection_model.keras"
model = load_model(model_path)

# Preprocess the input image
def preprocess_image(img_path):
    try:
        # Load image and resize it to match the model's input size
        img = image.load_img(img_path, target_size=(150, 150))  # Adjust to match your model's input size
        img_array = image.img_to_array(img)  # Convert image to NumPy array
        img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to match model input
        img_array /= 255.0  # Normalize pixel values
        return img_array
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None

@app.route('/prediction')
def prediction():
    return render_template('prediction.html', result=None, image_path=None)

# Define a route for the prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Ensure a secure file name and save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join('static/uploads', filename)
        file.save(file_path)
        
        # Preprocess the image for prediction
        img_array = preprocess_image(file_path)
        
        if img_array is None:
            return "Error in processing the image."

        try:
            # Make prediction
            prediction = model.predict(img_array)

            # Check prediction result (adjust according to model output)
            if prediction[0] < 0.5:
                result = "The image is detected as a Fake Face."
            else:
                result = "The image is detected as an Original Face."
        except Exception as e:
            print(f"Error during prediction: {e}")
            result = "Error during prediction"
        
        # Pass the result and image path to the template to display on the page
        print('uploads/' + filename)
        return render_template('prediction.html', result=result, image_path='uploads/' + filename)

# Create 'uploads' directory if it doesn't exist
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)





