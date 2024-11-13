import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from dbfunctions import *

app = Flask(__name__)
app.secret_key = "!@#@!#!"

# Folder to save uploaded images
IMAGE_FOLDER = 'static/images'

# Create the folder if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
    
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/')
def index():
    users = get_all_users()
    return render_template('index.html', users=users)
    
@app.route('/list')
def list_users():
    users = get_all_users()  # Fetch all users from the database
    return render_template('list.html', users=users)


def save_image_file(idno, base64_data):
    """Save base64 image data as a .png file using idno as the filename."""
    try:
        # Extract the base64 data if it includes a prefix
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        filename = f"{idno}.png"
        file_path = os.path.join(IMAGE_FOLDER, filename)
        
        # Decode the base64 data and write it to a file
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(base64_data))
        
        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

@app.route('/add', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        idno = request.form['idno']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        course = request.form['course']
        level = request.form['level']
        base64_image = request.form['image']
        
        # Check if the user already exists by ID number
        if get_user_by_idno(idno):
            flash("ID Number already exists!", "danger")
            return redirect(url_for('index'))
        
        # Save the image file and get the filename
        image_filename = save_image_file(idno, base64_image)
        if not image_filename:
            flash("Failed to save image.", "danger")
            return redirect(url_for('index'))

        # Insert user into the database with the saved image filename
        if add_user(idno, lastname, firstname, course, level, image_filename):
            flash("User added successfully!", "success")
        else:
            flash("Failed to add user.", "danger")
        return redirect(url_for('index'))
    
    # Render form for GET request
    return render_template('add_user.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
