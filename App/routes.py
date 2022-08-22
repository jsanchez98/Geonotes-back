import flask
from App import application, db, login#, csrf
from App.errors import APIError
from App.models import User, Post
from flask import render_template, request, jsonify, send_from_directory
import json
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf.csrf import generate_csrf, session, CSRFError

#@login.user_loader
#def load_user(id):
#    return User.query.get(int(id))

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

@application.route('/')
@application.route('/index')
def index():
    return application.send_static_file("index.html")

@application.route('/hello')
def hello():
    return "Hello, world!"

# Extract bodies from posts and send as a stringified list
@application.route('/posts')
@login_required
def sendPosts():
    posts = Post.query.filter_by(user_id=current_user.id)
    postBodies = list(map(lambda post: { "text" : post.body, "ID": post.id, "coordinates": post.location}, posts))
    postsString = json.dumps(postBodies)
    return postsString

@application.route('/addpost', methods=['POST'])
@login_required
def addPost():
    if request.method == 'POST':
        newPost = Post(body=request.json['text'], user_id=current_user.id,
                        location=request.json['coordinates'])
        db.session.add(newPost)
        db.session.commit()
        justMade = {
            "text": newPost.body,
            "ID": newPost.id,
            "coordinates": newPost.location
        }
        return json.dumps(justMade)

@application.route('/deletepost', methods=['POST'])
@login_required
def deletePost():
    if request.method == 'POST':
        id = request.json['postID']
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return sendPosts()

@application.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return "loggedin"
    user = User.query.filter_by(username=request.json["username"]).first()
    if user is None or not user.check_password(request.json["password"]):
        print("apierror")
        raise APIError("Invalid username or password")
    login_user(user)
    return "success"

@application.route('/logout')
@login_required
def logout():
    logout_user()
    return "success"

@application.route('/register', methods=['POST'])
def register():
    user = User.query.filter_by(username=request.json["username"]).first()
    if user is not None:
        raise APIError("Username taken")
    newUser = User(username=request.json["username"])
    newUser.set_password(request.json["password"])
    db.session.add(newUser)
    db.session.commit()
    return "success"

@application.route('/api/csrf')
def return_csrf():
    token = generate_csrf()
    
    response = jsonify({"detail": "CSRF token set"})
    response.headers.set("X-CSRFToken", token)
    return response
    

@application.errorhandler(APIError)
def handle_exception(err):
    return json.dumps({"message": err.description}), 400

@application.errorhandler(401)
def handle(err):
    return err

@application.errorhandler(CSRFError)
def handle_csrf_error(err):
    if application.config['WTF_CSRF_FIELD_NAME'] not in session:
        print("not in session")
    return json.dumps({"message": err.description}), 400