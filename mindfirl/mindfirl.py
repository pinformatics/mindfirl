import flask
from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import redis
from wtforms.fields import SelectField
from wtforms.fields import core, html5, simple
from wtforms import Form, validators, widgets
from urllib.parse import urlparse, urljoin
import os
from user import User, auth_user, register_user
from mutil import r
from flask_pymongo import PyMongo


app = Flask(__name__)
app.secret_key = 'a9%z$/`9h8Frnh893;*g7285h6'
app.config['MONGO_DBNAME'] = 'mindfirl'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mindfirl'

mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'

r.set('username_sysubo', 'passw0rd')
r.set('username_admin', 'admin')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
    return User.get(mongo=mongo, uid=user_id)


class LoginForm(Form):
    '''Form'''
    name = simple.StringField(
        label="Username",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="username cannot be empty"),
            validators.Length(max=20,min=5,message="The length of username should between 5 and 20")
        ],
        render_kw={"class":"form-control"}
    )

    pwd = simple.PasswordField(
        label="password",
        validators=[
            validators.DataRequired(message="password cannot be empty"),
            validators.Length(max=30,min=5,message="The length of password should between 5 and 30"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )


class SignupForm(Form):
    name = simple.StringField(
        label="Username",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="username cannot be empty"),
            validators.Length(max=20,min=5,message="The length of username should between 5 and 20")
        ],
        render_kw={"class":"form-control"}
    )

    pwd = simple.PasswordField(
        label="password",
        validators=[
            validators.DataRequired(message="password cannot be empty"),
            validators.Length(max=30,min=5,message="The length of password should between 5 and 30"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )


@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    if user.username == 'admin':
        users = mongo.db.mindfirl.users.find()
        return render_template('admin_dashboard.html', users=users)
    logout_link = '<a href="/logout">log out</a>'
    return "Dashboard. [" + user.username + "] " + logout_link


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="GET":
        form = LoginForm()
        return render_template("login.html",form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            user = auth_user(mongo=mongo, data=form.data)
            if user:
                login_user(user)
                #flask.flash('Logged in successfully.')
                next = flask.request.args.get('next')
                if not is_safe_url(next):
                    return flask.abort(400)
                return flask.redirect(next or flask.url_for('index'))
            else:
                flask.flash('Incorrect username or password. Please try again.')
        else:
            print(form.errors, "login error")
        return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flask.flash('Logged out successfully.')
    return redirect(url_for('login'))


@app.route('/register',methods=["GET","POST"])
def signup():
    if request.method =="GET":
        form = SignupForm()
        return render_template("register.html",form=form)
    else:
        form = SignupForm(formdata=request.form)
        if form.validate():
            user = register_user(mongo=mongo, data=form.data)
            if user:
                flask.flash('Register successful. Please login now.')
                return redirect(url_for('login'))
            else:
                print('failed.')
                flask.flash('Username exist.')
        else:
            print(form.errors, "signup error")
        return render_template("register.html", form=form)


@app.route('/project')
@login_required
def project():
    return render_template("project.html")


if __name__ == '__main__':
    app.run(debug=True)
