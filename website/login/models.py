from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlite3 as sql
import os

class User(UserMixin):
    def __init__(self, user):      #这里的user是数据库中读出来的用户数据组成的dictionary
        self.id = user["user_id"]
        self.name = user["user_name"] 
        self.email = user["user_email"]
        self.head = user["user_head"]
        self.password_hash = user["user_password"]
        self.identity = user["user_identity"]
        self.createtime = user["user_create_time"]
        
    def VerrifyPassword(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
        #return self.password_hash == password
    
    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db"))  
        cur = con.cursor()
        cur.execute('select * from UserInfo where user_id = ?', (user_id,))
        con.commit()
        user_info = cur.fetchone()
        if user_info == None:
            return None
        col_name_user = [tuple[0] for tuple in cur.description]
        user = dict(zip(col_name_user, user_info)) 
        return User(user)
