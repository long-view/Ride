from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models.user import User

class Bike:
    db_name = 'bike'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.biketype = db_data['biketype']
        self.description = db_data['description']
        self.bikepic = db_data['bikepic']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO bikes (biketype,description,bikepic,user_id) VALUES (%(biketype)s,%(description)s,%(bikepic)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM bikes"
    #     results = connectToMySQL(cls.db_name).query_db(query)
    #     all_bikes = []
    #     for row in results:
    #         # why would we have selected date??  must be changed
    #         print(row['date'])
    #         all_bikes.append(cls(row))

    #     return all_bikes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bikes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE bikes SET biketype=%(biketype)s, description=%(description)s, bikepic=%(bikepic)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM bikes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM bikes LEFT JOIN users on bikes.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        # print(results)
        bikes = []
        for row in results:
            
            bike = cls(row)
            
            n = {
                'id' : row['id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : ['users.updated_at'],
            }
            user = User(n)
            bike.user= user
            bikes.append(bike)

        return bikes
    
    @staticmethod
    def validate_bike(bike):
        is_valid = True
        if len(bike['biketype']) < 3:
            flash("Make/Model must be at least 3 characters","bike")
            is_valid=False
        if len(bike['description']) < 3:
            flash("Description must be at least 3 characters","bike")
            is_valid=False
        if bike['bikepic'] == "":
            flash("Plese upload an image","bike")
            is_valid =False
        return is_valid