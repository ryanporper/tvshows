import re
from flask import render_template, session, redirect, request, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tvshows import Tvshow
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/dashboard')
    return render_template("register.html")

@app.route('/register',methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['id'] = id
    return redirect('/dashboard')
    
@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    print("**********************************")
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['id'] = user.id
    return redirect('/dashboard')
    
@app.route("/dashboard")
def dashboard():
    if 'id' not in session:
        return redirect('/')
    data = {
        "id": session['id']
    }
    user = User.get_one_by_id(int(session['id']))
    return render_template("dashboard.html",user=user, tvshows=Tvshow.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')