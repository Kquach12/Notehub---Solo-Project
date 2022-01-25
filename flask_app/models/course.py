# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user 
# model the class after the friend table from our database


class Course:
    def __init__( self , data ):
        self.id = data['id']
        self.course_name = data['course_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM courses ORDER BY course_name ASC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query)
        # Create an empty list to append our instances of friends
        courses = []
        # Iterate over the db results and create instances of friends with cls.
        for course in results:
            courses.append( cls(course) )
        return courses

    @classmethod
    def save(cls, data):
        query = "INSERT INTO courses (course_name, created_at, updated_at) VALUES (%(course_name)s, NOW() , NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM courses WHERE id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_one_by_name(cls, data):
        query = "SELECT * FROM courses WHERE course_name = %(course_name)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
        
    @classmethod
    def update(cls, data):
        query = "UPDATE courses SET course_name = %(course_name)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM courses WHERE id = %(id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    @staticmethod
    def validate_course(course):
        is_valid = True
        # test whether a field matches the pattern
        query = "SELECT * FROM courses WHERE course_name = %(course_name)s;"
        results = connectToMySQL('notehub_schema').query_db(query,course)

        if len(course['course_name']) < 2:
            flash("Course name needs to be at least 2 characters", "chapter")
            is_valid = False
        elif len(course['course_name']) > 45:
            flash("Course name needs to be less than 45 characters", "chapter")
            is_valid = False
            
        else:
            if len(results) == 0:
                Course.save(course)

        return is_valid

