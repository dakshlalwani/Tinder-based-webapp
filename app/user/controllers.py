from flask import Blueprint, redirect, request, session, jsonify, render_template
from sqlalchemy.exc import IntegrityError
from app import db, requires_auth, app
from .models import User
from app.match.models import Match
from flask_recaptcha import ReCaptcha
import os
from sqlalchemy import or_,and_
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
mod_user = Blueprint('user', __name__)

app.config.update(dict(RECAPTCHA_ENABLED=True, RECAPTCHA_SITE_KEY="6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J", RECAPTCHA_SECRET_KEY="6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu", ))
recaptcha = ReCaptcha()
recaptcha.init_app(app)


@mod_user.route('/', methods=['GET'])
def homepage():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        string = "/profile/" + str(user.id)
        return redirect(string)
    return render_template('homepage.html')


@mod_user.route('/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        string = "/profile/" + str(user.id)
        return redirect(string)
    return render_template('login.html')


@mod_user.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        #return jsonify(success=False, message="%s not sent in the request" % e.args), 400
        return render_template('error.html', message="%s not sent in the request" % e.args)

    if recaptcha.verify():
        user = User.query.filter(User.email == email).first()
        if user is None or not user.check_password(password):
            return render_template('error.html', message="Invalid Credentials")

        session['user_id'] = user.id
        string = "/profile/" + str(user.id)
        return redirect(string)
    else:
        return render_template('error.html', message="Wrong reCAPTCHA")


@mod_user.route('/logout', methods=['GET'])
@requires_auth
def logout():
    session.pop('user_id')
    return redirect("/login")


@mod_user.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('register.html')
    try:
        name = request.form['firstName'] + " " + request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        gender = request.form['gender']
        age = request.form['age']
        preferred_min_age = request.form['preferred_min_age']
        preferred_max_age = request.form['preferred_max_age']
        preferred_gender = request.form['preferred_gender']
    except KeyError as e:
       return render_template('error.html', message="%s not sent in the request" % e.args)
       # return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    if '@' not in email:
       return jsonify(success=False, message="Please enter a valid email"), 400

    if recaptcha.verify():
        u = User(name, email, password, location, gender, age, preferred_min_age, preferred_max_age, preferred_gender)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError as e:
            return render_template('error.html', message="Username already taken!!")
        return redirect("/login")
    else:
        return render_template('error.html', message="Wrong reCAPTCHA")


@mod_user.route('/profile/<id>', methods=['GET', 'POST'])
@requires_auth
def get1_users(id):
    user_id = session['user_id']
    match1 = Match.query.filter(and_(Match.user1 == int(id) , Match.user2 == user_id)).first()
    match2 = Match.query.filter(and_(Match.user2 == int(id) , Match.user1 == user_id)).first()

    if user_id != int(id) and match1 == None and match2 == None:
        return render_template('error.html', message="You are not authorised to access this page")
    users = User.query.all()
    user_prof = User.query.filter(User.id == id).first()
    user_prof = user_prof.to_dict()
    if request.method == 'GET':
        return render_template('users1.html', user=user_prof, id=id)
    user_prof.name = request.form['firstName'] + " " + request.form['lastName']
    user_prof.email = request.form['email']
    user_prof.password = request.form['password']
    user_prof.location = request.form['location']
    user_prof.gender = request.form['gender']
    user_prof.age = request.form['age']
    user_prof.preferred_min_age = request.form['preferred_min_age']
    user_prof.preferred_max_age = request.form['preferred_max_age']
    user_prof.preferred_gender = request.form['preferred_gender']


@mod_user.route('/viewallusers', methods=['GET'])
@requires_auth
def viewallusers():
    users = User.query.all()
    arr = []
    logged_user = User.query.filter(User.id == session['user_id']).first()
    logged_user = logged_user.to_dict()
    for user in users:
        user = user.to_dict()
        if session['user_id'] != user['id'] and logged_user['preferred_gender'] == user['gender']:
            arr.append(user)
    return jsonify(success=True, users=arr)


@mod_user.route('/user/<id>', methods=['GET'])
@requires_auth
def get_users(id):
    if session['user_id'] == int(id):
        return render_template('user.html', id= id)
    return render_template('error.html', message="You are not authorised to access this page")


@mod_user.route('/profile/edit/<id>', methods=['GET', 'POST'])
@requires_auth
def edit_user(id):
    current_user_id = session['user_id']
    if current_user_id != int(id):
        return render_template('error.html', message="You are not authorised to access this page")
    users = User.query.all()
    current_user = User.query.filter(User.id == id).first()
    current_user = current_user.to_dict()
    if request.method == 'GET':
        return render_template('edit.html', user=current_user, id=id)
    try:
        name = request.form['name']
        location = request.form['location']
        gender = request.form['gender']
        age = request.form['age']
        preferred_min_age = request.form['preferred_min_age']
        preferred_max_age = request.form['preferred_max_age']
        preferred_gender = request.form['preferred_gender']
    except KeyError as e:
        return render_template('error.html', message="Request not sent")
    try:
        pic = request.files['User_Pic']
        filename = str(current_user_id) + ".jpg"
        pic.save(os.path.join(APP_ROOT, '../static/images/user_images', filename))
    except:
        pass

    current_user = User.query.filter(User.id == id).first()
    current_user.name = name
    current_user.location = location
    current_user.gender = gender
    current_user.age = age
    current_user.preferred_min_age = preferred_min_age
    current_user.preferred_max_age = preferred_max_age
    current_user.preferred_gender = preferred_gender
    db.session.commit()
    return redirect("/login")
