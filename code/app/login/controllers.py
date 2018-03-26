from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response,abort
from app.login.models import User
from app import db
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from werkzeug import secure_filename
from base64 import b64encode
import os

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg'])

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

mod_login = Blueprint('mod_login',__name__,template_folder='templates')
@mod_login.route('/')
def redirect_to():
    return redirect('/login')

@mod_login.route('/login/')
def check_session():
    if 'user_id' in session:
        r = make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
    else:           
        r = make_response(render_template('loginnew.html'))
    return r

@mod_login.route('/validate', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(email = username).first()
    if  user and user.check_password(password)==True:
        session['user_id'] = str(user.userid)
        session['type'] = "user"
        return make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
    else:
        flash('Invalid credentials','danger')
        r =  make_response(render_template('loginnew.html'))
        return r


@mod_login.route('/create',methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        image = request.files['inputFile']
        phone_no = request.form['phone']
        if image and allowed_filename(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
    except KeyError as e:
        flash('Invalid Details','danger')
        r =  make_response(render_template('loginnew.html'))
        return r

    user = User(name,username,password,filename,phone_no)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        flash('Email already exists','danger')
        r =  make_response(render_template('loginnew.html'))
        return r
    flash('Successfully created and logged in','success')    
    session['user_id'] = str(user.userid)
    session['type'] = "user"
    return make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))


@mod_login.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id',None)
    return redirect('/login')

@mod_login.route('/profile', methods=['GET'])
def profile():
    requests=User.query.filter_by(userid = int(session['user_id'])).first()
    image = requests.image
    if 'user_id' in session:
        return render_template('profile.html',requests=requests,image=image)
    else:
        return redirect('/login')

@mod_login.route('/searchval', methods=['POST'])
def search():
    username = request.form['Name']
    if 'user_id' in session:
        quer = User.query.filter(User.name.like("%" + username + "%")).all()
        return render_template('user.html',requests=quer,details=User.query.filter_by(userid = int(session['user_id'])).first())
    else:
        return redirect('/login')

@mod_login.route('/displayuser', methods=['GET'])
def allprofile():
    if 'user_id' in session:
        return render_template('user.html',requests=User.query.all(),details=User.query.filter_by(userid = int(session['user_id'])).first())
    else:
        return redirect('/login')
