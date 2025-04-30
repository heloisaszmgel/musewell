from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import Users
from flask import flash

class Notes:
    DB =  'musewell'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO notes (user_id, title, content) VALUES (%(user_id)s, %(title)s, %(content)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_all(cls, user_id):
        query = "SELECT * FROM notes LEFT JOIN users ON notes.user_id = users.id WHERE notes.user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL('musewell').query_db(query, data)
        if not results:
            return []
        user_notes = []
        for note in results:
            this_note = cls(note)
            user_notes.append(this_note)
        return user_notes

    
    @classmethod
    def get_one(cls, note_id):
        query = "SELECT * FROM notes WHERE id = %(id)s;"
        data = {'id': note_id}
        result = connectToMySQL('musewell').query_db(query, data)
        if not result:
            return None
        return cls(result[0])

    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        return connectToMySQL('musewell').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE notes SET title=%(title)s, content=%(content)s WHERE id = %(id)s;"
        return connectToMySQL('musewell').query_db(query, data)
    
    # @classmethod
    # def get_by_user_id(cls, user_id):
    #     query = "SELECT * FROM arbortrary WHERE user_id = %(user_id)s;"
    #     data = {'user_id': user_id}
    #     results = connectToMySQL('belt_exam').query_db(query, data)
    #     arbortraries = []
    #     for arbortrary in results:
    #         arbortraries.append(cls(arbortrary))
    #     return arbortraries
