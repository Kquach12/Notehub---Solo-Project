# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash 
from flask_app.models import chapter, school, course
# model the class after the friend table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fav_chapters = []
        self.fav_chapters_schools = []
        self.fav_chapters_courses = []
        self.fav_chapters_creators = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
        
    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE emails SET email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
    #     return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (user_id, chapter_id) VALUES (%(user_id)s, %(chapter_id)s)"
        return connectToMySQL('notehub_schema').query_db(query,data)

    @classmethod
    def unfavorite(cls, data):
        query = "DELETE FROM favorites WHERE user_id = %(user_id)s AND chapter_id = %(chapter_id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    @classmethod
    def get_user_with_chapters( cls , data ):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN chapters ON favorites.chapter_id = chapters.id LEFT JOIN courses ON chapters.course_id = courses.id LEFT JOIN schools ON chapters.school_id = schools.id LEFT JOIN users AS creators ON chapters.user_id = creators.id WHERE users.id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        user = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            chapter_data = {
                "id": row_from_db['chapters.id'],
                "title": row_from_db['title'],
                "availability": row_from_db['availability'],
                "created_at": row_from_db['created_at'],
                "updated_at": row_from_db['updated_at'],
                "user_id": row_from_db['user_id'],
                "school_id": row_from_db['school_id'],
                "course_id": row_from_db['course_id']
            }
            school_data = {
                "id": row_from_db['schools.id'],
                "school_name": row_from_db['school_name'],
                "created_at": row_from_db['schools.created_at'],
                "updated_at": row_from_db['schools.updated_at']
            }
            course_data = {
                "id": row_from_db['courses.id'],
                "course_name": row_from_db['course_name'],
                "created_at": row_from_db['courses.created_at'],
                "updated_at": row_from_db['courses.updated_at']
            }
            creator_data = {
                "id": row_from_db['creators.id'],
                "first_name": row_from_db['creators.first_name'],
                "last_name": row_from_db['creators.last_name'],
                "email": row_from_db['creators.email'],
                "password": row_from_db['creators.password'],
                "created_at": row_from_db['creators.created_at'],
                "updated_at": row_from_db['creators.updated_at']
            }
            user.fav_chapters.append( chapter.Chapter( chapter_data ) )
            user.fav_chapters_schools.append( school.School( school_data ) )
            user.fav_chapters_courses.append( course.Course( course_data ) )
            user.fav_chapters_creators.append( User( creator_data ) )
        return user



    @staticmethod
    def validate_email(user):
        is_valid = True
        # test whether a field matches the pattern
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('notehub_schema').query_db(query,user)
        if len(results) >= 1:
            flash("Email is taken!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match! ", "register")
            is_valid = False
        if len(user['password']) < 5:
            flash("Password must be at least 5 characters ", "register")
            is_valid = False
        if len(user['first_name']) < 1:
            flash("Please enter your first name ", "register")
            is_valid = False
        if len(user['first_name']) > 45:
            flash("Please keep your first name less than 45 characters ", "register")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Please enter your last name ", "register")
            is_valid = False
        if len(user['last_name']) > 45:
            flash("Please keep your last name less than 45 characters ", "register")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('notehub_schema').query_db(query,user)
        if len(results) == 0:
            flash("Account does not exist", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Please enter an email", "login")
            is_valid = False
        return is_valid