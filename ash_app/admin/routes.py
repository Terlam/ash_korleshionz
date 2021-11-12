from flask import Blueprint, render_template, request, redirect,url_for,flash, jsonify
from werkzeug.security import check_password_hash
from ash_app.forms import ProductUploadForm, CategoryUploadForm 
from ash_app.models import db, Category,Tag,Product,ProductImage
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

#Imports for Flask Login 
from flask_login import login_user, logout_user, current_user, login_required

admin = Blueprint('admin',__name__, template_folder= 'admin_templates')



@admin.route('/admins')
def dashboard():
    
    return render_template("admin.html")

@admin.route('/create-product', methods = ['GET','POST'])
def product():
    form = ProductUploadForm()
    form.category.choices = [(c.id, c.title) for c in Category.query.order_by('title')]
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            tags = form.tags.data
            category = form.category.data
            weight = form.weight.data
            price = form.price.data
            creation_cost = form.creation_cost.data
            stock = form.stock.data
            images = request.files.getlist('images')
            print(title)
            
            print(category)
           
            # Send Product to DB
            product = Product(title,description,stock,price,creation_cost,weight=weight,category_id=category)
            
            #get tags into table
            tag_list = [Tag(tag.strip()) for tag in tags.split(',')]
            db.session.flush()
             
             #add tags to product
            for i in tag_list:
                if i.title != Tag.query.filter(Tag.title == i.title).first():
                    product.product_has_tags.append(i) 

                # if tag exists already add old tag to product
                else: product.product_has_tags.append(Tag.query.filter(Tag.title == i.title).first())
           
            

            #Get Image to Cloudinary and URL to Table
            if request.files: 
                
                for file in images:
                    #Get name of file to reference image by
                    file_filename = file.filename

                    # cloudinary upload returns an object 😱 👇🏾
                    cloud_image = upload(file=file,public_id=f'ash-prods/{title}/{file_filename}', use_filename=True,unique_filename=True)

                    # Add Image to product_image table
                    product.image.append(ProductImage(cloud_image['url'],title=file_filename,product_id=product.id))
            else:
                print('No files here...')
                   
            db.session.add(product)
            db.session.commit()


            flash(f'You have successfully created a product {title}', 'product-created')

            return redirect(url_for('admin.product'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('product_form.html', form=form)

    # @admin.route('/upload',methods=['POST']):

@admin.route('/create-category', methods = ['GET','POST'])
def category():
    form = CategoryUploadForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            cat = form.category.data
         
            print(cat)
            
            categories = Category.query.filter(Category.title == cat).first()

            if not categories:
                category = Category(cat)
                db.session.add(category)
                db.session.commit()
                flash(f'You created the {cat} category','cat-success')
                return redirect(url_for('admin.category'))

            else:
                flash('Your already exists', 'cat-failed')
                return redirect(url_for('admin.category'))    
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('category_form.html', form = form)