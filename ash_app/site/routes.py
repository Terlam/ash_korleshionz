from flask import Blueprint, render_template
from ..models import Category, Product, ProductImage
# from flask_login.utils import login_required
"""
    Note that in the below code, 
    some arguments are specified when creating the Blueprint object
    The first argument, 'site', is the Blueprint's name,
    which is used by Flask's routing mechanism.

    The Second argument, __name__, is the Blueprint's import name,
    which Flask uses to locate the Blueprint's resources. 
"""

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    category = Category
    prods = Product.query
    product_image = ProductImage
    return render_template('index.html', category = category,prods = prods, product_image=product_image)

@site.route('/checkout')
# @login_required
def cart():
    return render_template('cart.html')

@site.route('/<prod>/details')
def details(prod):
    category = Category
    prods = Product.query
    imgs = ProductImage
    product = Product.query.filter(Product.title == prod).first()
    images = ProductImage.query.filter(ProductImage.product_id == product.id).all()
    return render_template('details.html', category = category, product = product, images=images, prods=prods,img=imgs)