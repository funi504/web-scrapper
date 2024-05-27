from http import client
import os
from routes.text_search import text_search
import flask
from flask import *
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from model import  db , User ,Tracking , Product
from config import ApplicationConfig ,configEmail
from routes.register import register_user
from routes.login import login_user
from routes.confirm_email import confirm_user_email
from routes.change_password import change_user_password
from routes.forgot_password import forgot_user_password
from routes.image_search import image_search
from routes.text_search import text_search
import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
server_session = Session(app)
mail = Mail(app)

app.secret_key = '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'
s = URLSafeTimedSerializer('Thisisasecret!-fjvnnjj2@123vvjk45ancnv9*')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register' ,methods = ['GET', 'POST'])
def create_user():
    resp = register_user( configEmail , app ,request ,bcrypt ,User, jsonify ,db , s , Message ,url_for ,mail , datetime)
    return resp

@app.route('/confirm_email/<token>' , methods=['GET', 'POST'])
def confirm_email(token):
    resp = confirm_user_email(token , s ,User ,db , datetime , SignatureExpired)
    return resp

@app.route('/change_password/<token>', methods=['POST', 'GET'])
def change_my_password(token):
    resp = change_user_password(token ,request , s , User , bcrypt ,db ,render_template)
    return resp

@app.route('/forget_password',methods=["POST"])
def forgot_my_password():
    resp = forgot_user_password(configEmail , app , request , s ,Message , url_for , mail , jsonify)
    return resp

@app.route('/login', methods=['POST'])
def log_user_in():
    resp = login_user(configEmail,app,request,User,bcrypt,jsonify,Message,s,url_for,mail,session,flask)
    return resp

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id")
    return "200"

@app.route('/image_search', methods=['GET','POST'])
def search_by_image():
    resp = image_search()
    return resp

@app.route('/text_search', methods=['GET','POST'])
def search_by_text():
    resp = text_search('phone case')
    return resp

# main driver function
if __name__ == '__main__':
 
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080 , debug=True)
