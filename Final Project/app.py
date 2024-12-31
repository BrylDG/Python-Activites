### app.py (Updated to Use Consolidated dbhelper.py)
import os
import qrcode
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dbhelper import *

app = Flask(__name__)
app.secret_key = "!@#@!#!"

# Folder to save uploaded images
IMAGE_FOLDER = 'static/images'
QR_FOLDER = 'static/qr_codes'

# Create folders if they don't exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route("/")
def index():
    return render_template("admin.html", pagetitle='User Login')

@app.route("/userlogin", methods=['POST'])
def userlogin():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['name'] = username
        flash("Login Accepted")
        return redirect("/userlist")
    else:
        flash("Login Failed")
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop('name', None)
    flash("Logged out")
    return redirect("/")

@app.route("/userlist")
def userlist():
    if not session.get('name'):
        return redirect("/")
    students = get_all_users()
    return render_template("index.html", students=students, pagetitle='User List')
    
@app.route("/studentlist")
def studentlist():
    if not session.get('name'):
        return redirect("/")
    students = get_all_users()
    return render_template("studentlist.html", students=students, pagetitle='User List')

@app.route("/adduser", methods=['GET', 'POST'])
def adduser_route():
    if request.method == 'POST':
        idno = request.form['idno']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        course = request.form['course']
        level = request.form['level']
        base64_image = request.form['image']

        if get_user_by_idno(idno):
            flash("ID Number already exists!", "danger")
            return redirect(url_for('adduser'))

        image_filename = save_image_file(idno, base64_image)
        qr_filename = generate_qr_code({'idno': idno, 'lastname': lastname, 'firstname': firstname, 'course': course, 'level': level})

        if add_user(idno, lastname, firstname, course, level, image_filename, qr_filename):
            flash("User added successfully!", "success")
        else:
            flash("Error adding user. Please try again.", "danger")

        return render_template("add.html", qr_image=f"{QR_FOLDER}/{qr_filename}")
    return render_template("add.html")

@app.route("/check_idno", methods=['POST'])
def check_idno():
    idno = request.form.get('idno')
    exists = get_user_by_idno(idno) is not None
    return jsonify({'exists': exists})

def save_image_file(idno, base64_data):
    try:
        base64_data = base64_data.split(',')[1] if ',' in base64_data else base64_data
        filename = f"{idno}.png"
        file_path = os.path.join(IMAGE_FOLDER, filename)
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(base64_data))
        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

def generate_qr_code(data):
    qr_data = f"IDNO: {data['idno']}, Lastname: {data['lastname']}, Firstname: {data['firstname']}, Course: {data['course']}, Level: {data['level']}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    filename = f"{data['idno']}.png"
    file_path = os.path.join(QR_FOLDER, filename)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(file_path)
    return filename

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
