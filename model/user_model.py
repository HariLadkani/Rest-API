import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost", 
                user="", 
                password="",
                database="flask_tutorial"
                )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successful")
        except:
            print("some error")
    def user_getall_model(self):
        self.cur.execute("SELECT * from user")
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload": result}, 200)
            res.headers["Acess-Control-Allow-Origin"] = "*"
            return res
        else:
            return make_response({"messsage": "No Data Found"}, 204)
        
    def user_getone_model(self, data):
        self.cur.execute(f"INSERT INTO user(name, email, role, password, phone) VALUES('{data['name']}','{data['email']}','{data['role']}','{data['password']}','{data['phone']}')")
        return make_response({"message": "user created"}, 201)

    def user_update_model(self, data):
        self.cur.execute(f"UPDATE user SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role='{data['role']}', password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated"}, 200)
        return make_response({"message":"NO UPDATE"}, 202)
    
    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM user WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"deleted well"}, 200)
        
        else:
            return make_response({"message":"nothing to delete"}, 202)
        
    def user_patch_model(self, data, id):
        query = "UPDATE user SET "
        for key in data:
            query += f"{key}='{data[key]}',"

        query = query[:-1] + f" WHERE id={id}"
        self.cur.execute(query)
        if self.cur.rowcount>0:
            return make_response(query, 201)

        else:
            return make_response(query, 202)
    
    def user_pagination_model(self, limit, page):
        start = int(page)*int(limit) - int(limit)
        query = f"SELECT * from user LIMIT {start}, {limit}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload": result, "page Number": page, "limit":limit}, 200)
            return res
        else:
            return make_response({"messsage": "No Data Found"}, 204)
        
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM user WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        data = result[0]
        expire = int((datetime.now() + timedelta(minutes=15)).timestamp())
        payload = {
            "payload": data,
            "exp":expire
        }
        token = jwt.encode(payload, "sagar", algorithm="HS256")
        return make_response({"token": token})
  

        
    
        
