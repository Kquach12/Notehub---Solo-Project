# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user 
# model the class after the friend table from our database


class Note:
    def __init__( self , data ):
        self.id = data['id']
        self.note = data['note']
        self.header = data['header']
        self.timestamp = data['timestamp']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chapter_id = data['chapter_id']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM notes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('notehub_schema').query_db(query)
        # Create an empty list to append our instances of friends
        notes = []
        # Iterate over the db results and create instances of friends with cls.
        for note in results:
            notes.append( cls(note) )
        return notes

    @classmethod   
    def get_all_with_chapter(cls, data):
        query = "SELECT * FROM notes LEFT JOIN chapters ON chapters.id = notes.chapter_id WHERE chapter_id = %(chapter_id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        notes = []
        # for row in results:
        for note in results:
            notes.append( cls(note) )
        return notes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO notes (note, header, timestamp, created_at, updated_at, chapter_id) VALUES (%(note)s, %(header)s, %(timestamp)s, NOW() , NOW(), %(chapter_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM notes WHERE id = %(id)s;"
        results = connectToMySQL('notehub_schema').query_db(query, data)
        return cls(results[0])
    
        
    @classmethod
    def update(cls, data):
        query = "UPDATE notes SET note = %(note)s, header = %(header)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('notehub_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s"
        return connectToMySQL('notehub_schema').query_db(query, data)

    # @classmethod 
    # def get_one_with_user(cls, data):
    #     query = "SELECT * FROM notes LEFT JOIN users ON users.id = notes.chapter_id WHERE notes.id = %(id)s;"
    #     results = connectToMySQL('notehub_schema').query_db(query, data)
    #     class = cls(results[0])
    #     for row in results:
    #         u = {
    #             "id": row['users.id'],
    #             "first_note": row['first_note'],
    #             "last_note": row['last_note'],
    #             "email": row['email'],
    #             "password": row['password'],
    #             "created_at": row['created_at'],
    #             "updated_at": row['updated_at']
    #         }
    #         class.users.append(user.User(u))
    #     return class

    # @staticmethod
    # def validate_class(class):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     query = "SELECT * FROM notes WHERE note = %(note)s;"
    #     results = connectToMySQL('notehub_schema').query_db(query,class)
    #     if 'under_30_minutes' not in class:
    #         flash("Please indicate the length of time! ", "class")
    #         is_valid = False
    #     if len(class['note']) < 3:
    #         flash("note needs to be at least 3 characters", "class")
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

