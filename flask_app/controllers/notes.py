from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_app.models.chapter import Chapter
from flask_app.models.course import Course
from flask_app.models.school import School


@app.route('/create/notes')
def create_notes():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    chapter = Chapter.get_one_recent(data)
    return render_template('create_notes.html',  chapter = chapter)


@app.route('/save/note', methods=["POST"])
def save_note_to_DB():
    data = {
        'header': request.form['header'],
        'note': request.form['note'],
        'timestamp': request.form['timestamp'],
        'chapter_id': request.form['chapter_id']
    }
    Note.save(data)
    return redirect('/create/notes')


@app.route('/view/note/<int:id>')
def view_note(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'chapter_id': id
    }
    chapter = Chapter.get_one_with_notes(data)
    favorites = Chapter.get_favorites_count(data)

    if (chapter.user_id != session['user_id'] and chapter.availability == 'private'):
        return redirect('/explore/notes')
    
    
    return render_template('view_note.html',  chapter = chapter, favorites = favorites['num_of_favs'])

@app.route('/edit/note/<int:id>')
def edit_note(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'chapter_id': id
    }
    chapter = Chapter.get_one_with_notes_school_course(data)

    if (chapter.user_id != session['user_id'] and chapter.availability == 'private'):
        return redirect('/explore/notes')
    

    return render_template('edit_chapter.html',  chapter = chapter)


@app.route('/edit/<int:chapter_id>', methods=["POST"])
def update_in_db(chapter_id):
    if not Chapter.validate_chapter(request.form) or not School.validate_school(request.form) or not Course.validate_course(request.form):
        return redirect(f'/edit/note/{chapter_id}')

    data_school_course = {
        "school_name": request.form['school_name'],
        "course_name": request.form['course_name']
    }
    school = School.get_one_by_name(data_school_course)
    course = Course.get_one_by_name(data_school_course)
    
    data_chapter = {
        'id': request.form['chapter_id'],
        'title': request.form['title'],
        'availability': request.form['availability'],
        "school_id": school.id,
        "course_id": course.id
    }
    Chapter.update(data_chapter)
    for i in range(int(request.form['num_of_notes'])):
        data_note = {
            'id': request.form['id'+str(i + 1)],
            'note': request.form['note'+str(i + 1)],
            'header': request.form['header'+str(i + 1)]
        }
        Note.update(data_note)
    return redirect(f"/view/note/{request.form['chapter_id']}")

