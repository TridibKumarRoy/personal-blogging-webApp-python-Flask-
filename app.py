from flask import Flask, render_template as rt,request, redirect, session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import json 
import os
from werkzeug.utils import secure_filename
import math

with open('config.json','r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER']=params['upload_location']

# Set the session lifetime to, for example, 30 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=300)


if bool(params["local_server"]["val"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["DBURI"]
else:
    # app.config['SQLALCHEMY_DATABASE_URI'] = params["ProdDBURI"]
    print("Failed to connect to the DB")
    
db = SQLAlchemy(app)


class Contacts(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50),  nullable=False)
    email=db.Column(db.String(50), unique=True, nullable=False)
    phone_num =db.Column(db.String(20),nullable=False)
    message= db.Column(db.String(500),  nullable=False)
    date =db.Column(db.DateTime,  nullable=False, default = datetime.now())
    
class Posts(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50),  nullable=False)
    content= db.Column(db.String(500),  nullable=False)
    slug= db.Column(db.String(50),  nullable=False)
    img_path= db.Column(db.String(500))
    date =db.Column(db.DateTime,  nullable=False, default = datetime.now())



def is_admin():
    return 'user' in session and session['user'] == params['username']

@app.context_processor
def inject_user():
    return {'isAdmin':is_admin(),'params':params}

@app.route("/")
def redir():
    return redirect('/1')

# Define a handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return rt('error.html',errcode=404,msg="Oops! The page you're looking for doesn't exist."), 404

# Define a handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    # Here you can log the error, if needed
    return rt('error.html',errcode=500,msg="Internal error"), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error, stack trace, and request details
    app.logger.error(f'Unhandled Exception: {e}', exc_info=True)
    
    # Return a custom 500 error page
    return rt('error.html',errcode=500,msg="Internal error"), 500
    

@app.route('/<int:page>')
def home(page):
    
    cp= page
    noOfPostsPPage = params['number_of_posts']
    end =cp* noOfPostsPPage
    start = end- noOfPostsPPage
    
    
    totalPosts = Posts.query.order_by(Posts.sno.desc()).all()
    posts = totalPosts[start:end]
    totalPages = int(math.ceil(len(totalPosts)/noOfPostsPPage))
    
    if page > totalPages - 1:
        disabled = 2
    elif page < 2:
        disabled = 1
    else:
        disabled = 0
    
    return rt('index.html',posts =posts,end=end,start=start,tp=totalPages,cp=cp,disabled =disabled )
    

@app.route('/about')
def about():
    return rt('about.html')

@app.route('/contact', methods =["GET","POST"])
def contact():
    if request.method=='POST':
        name =request.form.get('name')
        email=request.form.get('email')
        phone_num =request.form.get('phone_num')
        message= request.form.get('message')
        
        db.session.add(Contacts(name =name,email=email,phone_num =phone_num,message= message))
        db.session.commit()
        
    return rt('contact.html')

@app.route('/post/<string:post_slug>')
def post_route(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return rt('post.html', post = post)

@app.route("/login", methods=["GET","POST"])
def login():
    posts = Posts.query.all()
    contacts = Contacts.query.all()
    
    if 'user' in session and session['user']==params['username']:
        return rt('admin.html',posts=posts,contacts =contacts )
    
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')
        
        if name== params['username'] and password == params['password']:
            session['user'] = params['username']
            return rt('admin.html',posts=posts,contacts =contacts)
            
    return rt('login.html')

@app.route("/contact/delete/<int:sno>", methods=["GET","POST","DELETE"])
def deleteContact(sno):
    if 'user' in session and session['user']==params['username']:
        contact = Contacts.query.filter_by(sno =sno).first_or_404()
        db.session.delete(contact)
        db.session.commit()
        return redirect(url_for('login'))
    return rt('error.html',errcode=400,msg="Contact deletion failed"), 400

@app.route("/post/delete/<int:sno>", methods=["GET","POST","DELETE"])
def deletePost(sno):
    if 'user' in session and session['user']==params['username']:
        post = Posts.query.filter_by(sno =sno).first_or_404()
        db.session.delete(post)
        db.session.commit()
        if post.img_path:
            os.remove(f'./static/{post.slug}.png')
        return redirect(url_for('login'))
    return rt('error.html',errcode=400,msg="Contact deletion failed"), 400

@app.route('/post/new',methods=["GET","POST"])
def addPost():
    if 'user' in session and session['user']==params['username']:
        if request.method == "POST":
            lastpostSNo = Posts.query.order_by(Posts.sno.desc()).first()
            title = request.form.get('title')
            content = request.form.get('content')
            slug = f"{lastpostSNo.sno + 1}-{title.replace(' ', '-')[:10]}"
            
            image = request.files['image-file']
            # image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
            # image.save(f'./static/{secure_filename(image.filename)}')
            # imagePath= secure_filename(image.filename)
            if image:
                image.save(f'./static/{slug}.png')
                imagePath= f'{slug}.png'
            else:
                imagePath= f''
            
            post = Posts(title=title,content=content,slug=slug,img_path =imagePath)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('login'))
    return rt('error.html',errcode=400,msg="Adding new post failed"), 400

@app.route('/post/edit/<int:sno>',methods=["GET","POST","PUT"])
def editPost(sno):
    if 'user' in session and session['user']==params['username']:
        post = Posts.query.filter_by(sno = sno).first_or_404()
        posts = Posts.query.all()
        if request.method == "POST":
            title = request.form.get('title')
            content = request.form.get('content')
            imagePath = request.form.get('image')
            slug = request.form.get('slug')
            
            post.title =title
            post.content =content
            post.img_path =imagePath
            post.slug =slug
            post.date = datetime.now()
            
            db.session.commit()
            
            return redirect(url_for('login'))
        return rt('editpost.html',post=post)
    return rt('error.html',errcode=400,msg="Edit post failed"), 400

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

if(__name__=="__main__"):
    app.run(debug=True,port=params["port"],host=params["host"])