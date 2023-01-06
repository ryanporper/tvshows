from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db_name = 'tvshows'

class Tvshow:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tvshows JOIN users on users.id = user_id;"
        result = connectToMySQL(db_name).query_db(query)
        tvshows = []
        for row_from_db in result:
            current_tvshow = cls(row_from_db)
            user_data = {
                **row_from_db,
                'id': row_from_db['users.id'],
                'created_at': row_from_db['users.created_at'],
                'updated_at': row_from_db['users.updated_at']
            }
            tvshows_user = User(user_data)
            current_tvshow.owner = tvshows_user
            tvshows.append(current_tvshow)
        return tvshows

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM tvshows JOIN users on users.id = user_id WHERE tvshows.id = %(id)s;"
        result = connectToMySQL(db_name).query_db(query,data)
        tvshow = cls(result[0])
        row_from_db = result[0]

        user_data = {
            **row_from_db,
            'id': row_from_db['users.id'],
            'created_at': row_from_db['users.created_at'],
            'updated_at': row_from_db['users.updated_at']
        }
        owner = User(user_data)
        tvshow.owner = owner
        return tvshow

    @classmethod
    def delete_by_id(cls, data):
        query = "DELETE FROM tvshows WHERE id = %(id)s"
        return connectToMySQL(db_name).query_db(query, data) 

    @classmethod
    def save(cls,data):
        query = "INSERT INTO tvshows (title, network, release_date, description, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);"
        return connectToMySQL(db_name).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE tvshows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, user_id = %(user_id)s WHERE id = %(id)s"
        return connectToMySQL(db_name).query_db(query,data)

    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters.","new")
        if len(data['network']) < 2:
            is_valid = False
            flash("Network must be at least 2 characters.","new")
        if len(data['description']) < 2:
            is_valid = False
            flash("Description must be at least 2 characters.","new")
        if len(data['release_date']) < 1:
            is_valid = False
            flash("You must enter a date.","new")
        return is_valid


    
        

