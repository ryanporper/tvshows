from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.controllers import tvshows_controller
from flask_app.models import tvshows

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db_name = 'tvshows'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL(db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(db_name).query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users

    @classmethod
    def get_one_by_id(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id':id}
        result = connectToMySQL(db_name).query_db(query,data)
        user = cls(result[0])
        return user

    @classmethod
    def get_one_by_id_with_tvshows(cls, data):
        query = "SELECT * FROM users LEFT JOIN tvshows on users.id = tvshows.user_id WHERE users.id = %(id)s;"
        result = connectToMySQL(db_name).query_db(query,data)
        user = cls(result[0])
        list_of_tvshows = []
        if result[0]['tvshows.id'] != None:
            for row_from_db in result:
                tvshow_data = {
                    **row_from_db,
                    'id' : row_from_db['tvshows.id'],
                    'created_at' : row_from_db['created_at'],
                    'updated_at' : row_from_db['updated_at'],
                }
                this_tvshow = tvshows.Tvshow.Tvshow(tvshow_data)
                list_of_tvshows.append(this_tvshow)
        user.tvshows = list_of_tvshows
        return user


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters.","register")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.","register")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords do not match!","register")
        return is_valid