from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

class Tracking(db.Model):
    __tablename__ = "tracking"
    tracking_id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.String(50), primary_key=True, nullable=False)
    product_name = db.Column(db.Text, nullable=False)
    product_url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Text, nullable=False)
    num_ratings = db.Column(db.Text, nullable=False)
    store = db.Column(db.Text, nullable=False)

