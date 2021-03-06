# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user 
# model the class after the friend table from our database


class School:
    def __init__( self , data ):
        self.id = data['id']
        self.school_name = data['school_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM schools ORDER BY school_name ASC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query)
        # Create an empty list to append our instances of friends
        schools = []
        # Iterate over the db results and create instances of friends with cls.
        for school in results:
            schools.append( cls(school) )
        return schools


    @classmethod
    def save(cls, data):
        query = "INSERT INTO schools (school_name, created_at, updated_at) VALUES (%(school_name)s, NOW() , NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM schools WHERE id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_by_name(cls, data):
        query = "SELECT * FROM schools WHERE school_name = %(school_name)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
    
        
    @classmethod
    def update(cls, data):
        query = "UPDATE schools SET school_name = %(school_name)s,  updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM schools WHERE id = %(id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    @staticmethod
    def validate_school(school):
        is_valid = True
        query = "SELECT * FROM schools WHERE school_name = %(school_name)s;"
        results = connectToMySQL('notehub_schema').query_db(query,school)

        if len(school['school_name']) < 2:
            flash("School name needs to be at least 2 characters", "chapter")
            is_valid = False

        elif len(school['school_name']) > 45:
            flash("School name needs to be less than 45 characters", "chapter")
            is_valid = False
            
        else:
            #if school has not been saved by other user
            if len(results) == 0:
                School.save(school)
        
        return is_valid


