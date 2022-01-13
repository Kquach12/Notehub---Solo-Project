from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.chapter import Chapter
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods = ["POST"])
def register_user():
    if not User.validate_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        user = User.get_one(data)
        recent_chapters = []
        chapters = Chapter.get_all_with_school_and_course(data)
        counter = 0
        for i in reversed(range(len(chapters))):
            if counter == 2:
                break
            recent_chapters.append(chapters[i])
            counter+=1
        return render_template("dashboard.html", user = user, chapters = recent_chapters)
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/favorites')
def show_favorites():
    data={
        "id": session['user_id']
    }
    user = User.get_user_with_chapters(data)
    return render_template('favorites.html', user = user)

@app.route("/favorite/note", methods = ["POST"])
def favorite_note():
    data = {
        "chapter_id": request.form['chapter_id'],
        "user_id": session['user_id']
    }
    User.add_favorite(data)
    return redirect("/explore/notes")

@app.route('/unfavorite/chapter/<int:chapter_id>')
def unfavorite_chapter(chapter_id):
    data = {
        "chapter_id": chapter_id,
        "user_id": session['user_id']
    }
    User.unfavorite(data)
    return redirect('/favorites')
