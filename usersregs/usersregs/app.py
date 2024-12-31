from flask import Flask,render_template,request,redirect,session,flash
from dbhelper import *

app = Flask(__name__)
app.secret_key = "!@#@!#!"

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate' #http v1.1
    response.headers['Pragma'] = 'no-cache'
    #response.headers['expiry'] = "0"
    return response

@app.route("/adduser",methods=['POST'])
def adduser()->None:
    fname:str = request.form['fname']
    username:str = request.form['username']
    password:str = request.form['password']
    ok:bool = addnewuser(fname,username,password)
    message:str = "New User Added" if ok else "Error Adding User"
    flash(message)
    return redirect("/userlist")

@app.route("/logout")
def logout()->None:
    session['name'] = None
    flash("Logged out")
    return redirect("/")


@app.route("/userlogin",methods=['POST'])
def userlogin()->None:
    username:str = request.form['username']
    password:str = request.form['password']
    if len(validateuser(username,password))>0:
        session['name'] = username
        flash("Login Accepted")
        return redirect("/userlist")
    else:
        flash("Login Failed")
        return redirect("/")

@app.route("/userlist")
def userlist()->None:
    if not session.get('name'):
        return redirect("/")
    else:
        users:list = getall_record('users')
        return render_template("index.html",users=users,pagetitle='users list')

@app.route("/")
def index()->None:
    return render_template("login.html",pagetitle='users login')

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")