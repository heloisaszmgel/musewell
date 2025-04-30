from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template ('index.html')

@app.route("/submit", methods=["POST"])
def register_login():
    if request.form["action"] == "register":
        is_valid = Users.validate_user(request.form)
        if not is_valid:
            return redirect ("/")
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash("Passwords do not match", "registration_failed")
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password" : pw_hash,
            "confirm_password" : request.form['confirm_password'],
        }
        users_id = Users.save(data)
        session['user_id'] = users_id
        return redirect("/dashboard")
        
    else:
        data = {
            "email" : request.form["email"],
        }
        this_user = Users.get_by_email(data)
        if not this_user:
            flash("Invalid Email", 'login_failed')
            return redirect("/")
        if not bcrypt.check_password_hash(this_user.password, request.form['password']):
            flash("Invalid Password", 'login_failed')
            return redirect("/")
        session['user_id'] = this_user.id
        return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
