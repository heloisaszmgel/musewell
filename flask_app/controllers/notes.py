from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.note import Notes
from flask_app.models.user import Users
from flask import flash

#app.route after the user register or login
@app.route('/dashboard')
def dashboard():
    if  'user_id' not in session:
        return redirect('/')
    logged_in_user = Users.get_one(session['user_id'])
    return render_template("dashboard.html", notes=Notes.get_all(session['user_id']), user=logged_in_user)

#app,route for the creation of the new trees
@app.route('/new/note', methods=['GET' , 'POST'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        data = {
            'user_id': session['user_id'],
            'title': request.form['title'],
            'content': request.form['content'],
        }
        Notes.save(data)
        return redirect('/dashboard')
    else:
        logged_in_user = Users.get_one(session['user_id'])
        return render_template("new_note.html", user=logged_in_user )

#show details
@app.route('/display_one/<int:id>')
def show_one(id):
    if 'user_id' not in session:
        return redirect('/')
    note = Notes.get_one(id)
    logged_in_user = Users.get_one(session['user_id'])
    return render_template("display_one.html", note = note, user=logged_in_user )

# #delete
@app.route('/note/delete/', methods=['POST'])
def destroy():
    Notes.delete(request.form)
    return redirect('/dashboard')

#edit route
@app.route('/note/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    note = Notes.get_one(id)
    logged_in_user = Users.get_one(session['user_id'])
    return render_template('edit.html', note = note, user=logged_in_user )

#update route (for after editing)
@app.route('/note/update', methods=['POST'])
def update():
    Notes.update(request.form)
    return redirect ('/dashboard')

