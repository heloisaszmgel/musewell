from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    DB =  'musewell'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.notes = []
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True 
        if len(user['first_name'].strip() ) < 2:
            flash("First name must be at least 2 characters.", "registration_failed")
            is_valid = False
        if len(user['last_name'].strip()) < 2:
            flash("Last name must be at least 2 characters.", "registration_failed")
            is_valid = False
        if not user['email']:
            flash("Email cannot be blank", "registration_failed")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "registration_failed")
            is_valid = False
        else:
            existing_user = Users.get_by_email({'email': user['email']})
            if existing_user:
                flash("Email already registered. Please log in.", "registration_failed")
                is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "registration_failed")
            is_valid = False
        return is_valid 
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('musewell').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL('musewell').query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    