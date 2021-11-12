from os import PRIO_PGRP
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets module (Given by Python)
import secrets

# Imports for Login Manager
from flask_login import UserMixin

# Imports for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
# from flask_marshmallow import Marshmallow



db = SQLAlchemy()
login_manager = LoginManager()
# ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable= True, default = '')
    admin = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_logged_in = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    measurement = db.relationship('Measurement', backref = 'Buyer', lazy = "dynamic")
    orders = db.relationship('Orders', backref = 'Customer', lazy = "dynamic")

    def __init__(self, email,first_name = '', last_name = '', id ='', password = '', token = '', admin=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.admin = admin
        
    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.'

class Measurement(db.Model):
    id = db.Column(db.String, primary_key = True)
    person = db.Column(db.String(150))
    height = db.Column(db.Numeric(precision=6, scale=2))
    weight = db.Column(db.Numeric(precision=6, scale=2))
    nip_to_nip = db.Column(db.Numeric(precision=6, scale=2))
    waist = db.Column(db.Numeric(precision=6, scale=2))
    shoulder_to_shoulder_back = db.Column(db.Numeric(precision=6, scale=2))
    shoulder_to_waist = db.Column(db.Numeric(precision=6, scale=2))
    hips = db.Column(db.Numeric(precision=6, scale=2))
    trouser_length = db.Column(db.Numeric(precision=6, scale=2))
    waist_to_knee = db.Column(db.Numeric(precision=6, scale=2))
    bar = db.Column(db.Numeric(precision=6, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,person,height,weight,nip_to_nip,bust,waist,shoulder_to_shoulder_back,shoulder_to_waist,hips,trouser_length,waist_to_knee,bar,user_token,id=''):
        self.id = self.set_id()
        self.person = person
        self.height = height
        self.weight = weight
        self.nip_to_nip = nip_to_nip
        self.bust = bust
        self.waist = waist
        self.shoulder_to_shoulder_back = shoulder_to_shoulder_back
        self.shoulder_to_waist = shoulder_to_waist
        self.hips = hips
        self. trouser_length = trouser_length
        self.waist_to_knee = waist_to_knee
        self.bar = bar
        self.user_token = user_token

    def __repr__(self):
        return f"{self.name}'s measuerements have been added: "

    def set_id(self):
        return secrets.token_urlsafe()



# Many to Many √
OrderDetail = db.Table("Order_Detail", 
    db.Column('id',db.Integer, primary_key = True),
    db.Column('quantity',db.Integer, nullable = False, default = 1),
    db.Column('discount',db.Numeric(precision=10, scale = 2), nullable = True),
    db.Column('order_id',db.String, db.ForeignKey('orders.id'), nullable = False),
    db.Column('product_id',db.String, db.ForeignKey('product.id'), nullable = False)
    )
    
 

class Orders(db.Model):
    id = db.Column(db.String, primary_key = True)
    status = db.Column(db.String(200), nullable = True)
    order_date =  db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    shipped_date =  db.Column(db.DateTime, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    order_detail = db.relationship('Product', secondary = OrderDetail, backref = 'Purchases', lazy = "dynamic")

    def __init__(self,status,order_date,shipped_date,user_token,id=''):
        self.id = self.set_id()
        self.status = status
        self.order_date = order_date
        self.shipped_date = shipped_date
        self.user_token = user_token

    def __repr__(self):
        return f'The order has been added.'

    def set_id(self):
        return secrets.token_urlsafe()

   
class Category(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(30), nullable = False, default = 'Traditional')
    product = db.relationship('Product', backref = 'Category', lazy = "dynamic")

    def __init__(self,title,id=''):
        self.id = self.set_id()
        self.title = title

    def __repr__(self):
        return f'The {self.title} category has been added.'

    def set_id(self):
        return secrets.token_urlsafe()        

#Many to many
ProductHasTags= db.Table('Product_Has_Tags',
    db.Column('id',db.Integer, primary_key = True),
    db.Column('tag_id',db.String, db.ForeignKey('tag.id'), nullable = False),
    db.Column('product_id',db.String, db.ForeignKey('product.id'), nullable = False)
)



class Product(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(2000), nullable = True)
    stock =  db.Column(db.Integer, nullable = False, default = 1)
    price =  db.Column(db.Numeric(precision=10, scale=2))
    creation_cost =  db.Column(db.Numeric(precision=10, scale=2))
    weight = db.Column(db.Numeric(precision=6, scale=2))
    category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable = False)
    image = db.relationship('ProductImage', backref = 'Product', lazy = True)
    product_has_tags = db.relationship('Tag', secondary= ProductHasTags,backref='prods',lazy=True)

    def __init__(self,title,description,stock,price,creation_cost,weight,category_id,id=''):
        self.id = self.set_id()
        self.title = title
        self.description = description
        self.stock = stock
        self.price = price
        self.creation_cost = creation_cost
        self.weight = weight
        self.category_id = category_id

    def __repr__(self):
        return f'The following product has been added: {self.title}'

    def set_id(self):
        return secrets.token_urlsafe()



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False, default = "")
    # product_has_tags = db.relationship('Product', secondary = Product_Has_Tags, backref = 'tagged', lazy = "dynamic")

    def __init__(self,title,id =''):
        self.id = self.set_id()
        self.title = title

    def __repr__(self):
        return f'The {self.title} tag has been added.'

    def set_id(self):
        return secrets.token_urlsafe()  



class ProductImage(db.Model):
    image_url = db.Column(db.String, primary_key = True)
    title = db.Column(db.String)
    product_id = db.Column(db.String, db.ForeignKey('product.id'), nullable = False)

    def __init__(self, image_url,title,product_id):
        self.image_url = image_url
        self.title = title
        self.product_id = product_id

# Creation of API Schema via the Marshmallow Object
# class ProductSchema(ma.Schema):
#     class Meta:
#         fields = ['id','title','description','stock','price','creation_cost','image','weight','category_id']


# product_schema = ProductSchema()

# products_schema = ProductSchema(many=True)
