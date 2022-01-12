# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user, note, school, course 
# model the class after the friend table from our database


class Chapter:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.availability = data['availability']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.school_id = data['school_id']
        self.course_id = data['course_id']
        self.users = []
        self.notes = []
        self.schools = []
        self.courses = []
        self.fav_users = 0

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM chapters;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query)
        # Create an empty list to append our instances of friends
        chapters = []
        # Iterate over the db results and create instances of friends with cls.
        for chapter in results:
            chapters.append( cls(chapter) )
        return chapters

    @classmethod
    def get_other_public(cls, data):
        query = "SELECT * FROM chapters LEFT JOIN courses ON chapters.course_id = courses.id LEFT JOIN schools ON chapters.school_id = schools.id LEFT JOIN users ON chapters.user_id = users.id WHERE availability = 'public' AND user_id <> %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query, data)
        # Create an empty list to append our instances of friends
        chapters = []
        # Iterate over the db results and create instances of friends with cls.
        for i in range(len(results)):
            chapters.append(cls(results[i]))
            u = {
                "id": results[i]['users.id'],
                "first_name": results[i]['first_name'],
                "last_name": results[i]['last_name'],
                "email": results[i]['email'],
                "password": results[i]['password'],
                "created_at": results[i]['users.created_at'],
                "updated_at": results[i]['users.updated_at']
            }
            s = {
                "id": results[i]['schools.id'],
                "school_name": results[i]['school_name'],
                "created_at": results[i]['schools.created_at'],
                "updated_at": results[i]['schools.updated_at']
            }
            c = {
                "id": results[i]['courses.id'],
                "course_name": results[i]['course_name'],
                "created_at": results[i]['courses.created_at'],
                "updated_at": results[i]['courses.updated_at']
            }
            chapters[i].users.append(user.User(u))
            chapters[i].schools.append(school.School(s))
            chapters[i].courses.append(course.Course(c))
            
        return chapters

    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM chapters WHERE user_id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query, data)
        # Create an empty list to append our instances of friends
        chapters = []
        # Iterate over the db results and create instances of friends with cls.
        for chapter in results:
            chapters.append( cls(chapter) )
        return chapters

    @classmethod
    def save(cls, data):
        query = "INSERT INTO chapters (title, availability, created_at, updated_at, user_id, school_id, course_id) VALUES (%(title)s, %(availability)s, NOW() , NOW(), %(user_id)s, %(school_id)s, %(course_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM chapters WHERE id = %(chapter_id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_one_recent(cls, data):
        query = "SELECT * FROM chapters WHERE user_id =%(user_id)s ORDER BY id DESC LIMIT 0,1;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
    
        
    @classmethod
    def update(cls, data):
        query = "UPDATE chapters SET title = %(title)s, availability = %(availability)s, created_at = %(created_at)s,  updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM chapters WHERE id = %(id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    @classmethod 
    def get_one_with_notes(cls, data):
        query = "SELECT * FROM chapters LEFT JOIN notes ON chapters.id = notes.chapter_id WHERE chapter_id = %(chapter_id)s ORDER BY notes.id ASC;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        if len(results) > 0:
            chapter = cls(results[0])
            for row in results:
                n = {
                    "id": row['notes.id'],
                    "note": row['note'],
                    "header": row['header'],
                    "timestamp": row['timestamp'],
                    "created_at": row['notes.created_at'],
                    "updated_at": row['notes.updated_at'],
                    "chapter_id": row['chapter_id']
                }
                chapter.notes.append(note.Note(n))
        else:
            chapter = Chapter.get_one(data)
            
        return chapter

    @classmethod 
    def get_one_with_notes_school_course(cls, data):
        query = "SELECT * FROM chapters LEFT JOIN courses ON chapters.course_id = courses.id LEFT JOIN schools ON chapters.school_id = schools.id LEFT JOIN notes ON chapters.id = notes.chapter_id WHERE chapters.id = %(chapter_id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        if len(results) > 0:
            chapter = cls(results[0])
            for row in results:
                n = {
                    "id": row['notes.id'],
                    "note": row['note'],
                    "header": row['header'],
                    "timestamp": row['timestamp'],
                    "created_at": row['notes.created_at'],
                    "updated_at": row['notes.updated_at'],
                    "chapter_id": row['chapter_id']
                }
                s = {
                    "id": row['schools.id'],
                    "school_name": row['school_name'],
                    "created_at": row['schools.created_at'],
                    "updated_at": row['schools.updated_at']
                }
                c = {
                    "id": row['courses.id'],
                    "course_name": row['course_name'],
                    "created_at": row['courses.created_at'],
                    "updated_at": row['courses.updated_at']
                }
                chapter.notes.append(note.Note(n))
                chapter.schools.append(school.School(s))
                chapter.courses.append(course.Course(c))
        else:
            chapter = Chapter.get_one(data)
            
        return chapter


    @classmethod 
    def get_all_with_school_and_course(cls, data):
        query = "SELECT * FROM chapters LEFT JOIN courses ON chapters.course_id = courses.id LEFT JOIN schools ON chapters.school_id = schools.id WHERE user_id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        chapters = []
        for i in range(len(results)):
            chapters.append(cls(results[i]))
            s = {
                "id": results[i]['schools.id'],
                "school_name": results[i]['school_name'],
                "created_at": results[i]['schools.created_at'],
                "updated_at": results[i]['schools.updated_at']
            }
            c = {
                "id": results[i]['courses.id'],
                "course_name": results[i]['course_name'],
                "created_at": results[i]['courses.created_at'],
                "updated_at": results[i]['courses.updated_at']
            }
            chapters[i].schools.append(school.School(s))
            chapters[i].courses.append(course.Course(c))
            
        return chapters


    @classmethod
    def get_favorites_count( cls , data ):
        query = "SELECT COUNT(user_id) AS num_of_favs FROM favorites WHERE chapter_id = %(chapter_id)s;"
        results = connectToMySQL('notehub_schema').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        favorites = results[0]
        return favorites
        

    # @staticmethod
    # def validate_class(class):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     query = "SELECT * FROM chapters WHERE title = %(title)s;"
    #     results = connectToMySQL('notehub_schema').query_db(query,class)
    #     if 'under_30_minutes' not in class:
    #         flash("Please indicate the length of time! ", "class")
    #         is_valid = False
    #     if len(class['title']) < 3:
    #         flash("title needs to be at least 3 characters", "class")
    #         is_valid = False
    #     if len(class['description']) < 5:
    #         flash("Description must be at least 5 characters ", "class")
    #         is_valid = False
    #     if len(class['instruction']) < 5:
    #         flash("Instruction must be at least 5 characters", "class")
    #         is_valid = False
    #     if len(class['created_at']) < 1:
    #         flash("Please enter a date", "class")
    #         is_valid = False

    #     return is_valid

