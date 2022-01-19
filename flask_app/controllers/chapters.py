from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.chapter import Chapter
from flask_app.models.school import School
from flask_app.models.course import Course
from flask_app.controllers import notes


@app.route('/create/chapter')
def create_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    return render_template('create_chapter.html', user = user)

@app.route('/create', methods = ["POST"])
def add_to_db():
    if not Chapter.validate_chapter(request.form) or not School.validate_school(request.form) or not Course.validate_course(request.form):
        return redirect('/create/chapter')

    data_school_course = {
        "school_name": request.form['school_name'],
        "course_name": request.form['course_name']
    }

    school = School.get_one_by_name(data_school_course)
    course = Course.get_one_by_name(data_school_course)
    
    data = {
        "title": request.form['title'],
        "availability": request.form['availability'],
        "user_id": session['user_id'],
        "school_id": school.id,
        "course_id": course.id
    }
    Chapter.save(data)
    return redirect('/create/notes')


@app.route('/all/notes')
def all_notes():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    chapters = Chapter.get_all_with_school_and_course(data)
    return render_template('all_notes.html', chapters = chapters)


@app.route('/explore/notes')
def explore():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    chapters = Chapter.get_other_public(data)
    user = User.get_user_with_chapters(data)
    favorites_id = []
    for favorite in user.fav_chapters:
        favorites_id.append(favorite.id)
    return render_template('explore.html', chapters = chapters, favorites = favorites_id)



@app.route('/delete/note/<int:id>')
def delete_chapter(id):
    data = {
        "id": id
    }
    Chapter.delete(data)
    return redirect('/all/notes')
