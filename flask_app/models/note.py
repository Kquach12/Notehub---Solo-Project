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
