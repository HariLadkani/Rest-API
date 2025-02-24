from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file
import json
from datetime import datetime


obj = user_model()
auth = auth_model()
@app.route("/user/getall")
@auth.token_auth("/user/getall")
def user_controller_signup():
    return obj.user_getall_model()

@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    return obj.user_getone_model(request.form)
 

@app.route("/user/update", methods=["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)
  

@app.route("/user/delete/<id>", methods=["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)


@app.route("/user/patch/<id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)


@app.route("/user/getall/limit/<limit>/page/<page>", methods=["GET"])
def user_pagination(limit, page):
    return obj.user_pagination_model(limit, page)  

@app.route("/user/<uid>/upload/avatar", methods=["PUT"])
def user_upload_avatar_controller(uid):
    file = request.files["avatar"]
    
    unique_filename = str(datetime.now().timestamp()).replace(".", "")
    ext = file.filename.split(".")[-1]
    file.save(f"uploads/{unique_filename}.{ext}")
    return f"uploads/{unique_filename}.{ext}"


@app.route("/uploads/<filename>")
def user_getavatar_controler(filename):
    return send_file(f".\\uploads\\{filename}")

@app.route("/user/login", methods=["POST"])
def user_login_controller():
    return obj.user_login_model(request.form)
    