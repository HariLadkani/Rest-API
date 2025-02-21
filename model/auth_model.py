import mysql.connector
import json
import re

from flask import make_response, request
import jwt
class auth_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost", 
                user="springstudent", 
                password="springstudent",
                database="flask_tutorial"
                )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("connection successful")
        except:
            print("some error")

    def token_auth(self, endpoint):
        def inner1(func):
            def inner2(*args):
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token  = authorization.split(" ")[1]
                    jwt_decoded = jwt.decode(token, "sagar", algorithms="HS256")
                    print(jwt_decoded)
                    role_id = jwt_decoded["payload"]['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint='{endpoint}'")
                    roles = self.cur.fetchall()
                
                    if len(roles) > 0:
                        roles = json.loads(roles[0]["roles"])
                        if role_id in roles:
                            return func(*args)
                        else:
                            return make_response({"ERROR":"UNAUTHORIZED REQUEST"}, 401)

                    else:
                        return make_response({"ERROR":"UNKNOWN ENDPOINT"}, 404)
                else:
                    return make_resonse({"ERROR": "INVALID_TOKEN"}, 401)

            return inner2
        
        return inner1
