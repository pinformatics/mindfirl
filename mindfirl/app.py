import flask
from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import redis
from wtforms.fields import SelectField
from wtforms.fields import core, html5, simple
from wtforms import Form, validators, widgets
from urllib.parse import urlparse, urljoin
import os


if 'DYNO' in os.environ:
    ENV = 'production'
else:
    ENV = 'development'

if ENV == 'production':
    r = redis.from_url(os.environ.get("REDIS_URL"))
elif ENV == 'development':
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


app = Flask(__name__)
app.secret_key = 'a9%z$/`9h8Frnh893;*g7285h6'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'

r.set('username_sysubo', 'passw0rd')
r.set('username_admin', 'admin')


class User(object):
    def __init__(self, username):
        self.username = username
        self.id = username


    @staticmethod
    def get(uid):
        if True:
            return User(uid)
        return None


    __hash__ = object.__hash__


    @property
    def is_active(self):
        return True


    @property
    def is_authenticated(self):
        return True


    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


    def __eq__(self, other):
        '''
        Checks the equality of two `User` objects using `get_id`.
        '''
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented


    def __ne__(self, other):
        '''
        Checks the inequality of two `User` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


def auth_user(data):
    username = data['name']
    password = data['pwd']
    correct_pwd = r.get('username_' + username)
    if not correct_pwd:
        return None
    if password != correct_pwd:
        print("password: %s" % password)
        print("correct pwd: %s" % correct_pwd)
        return None
    return User(username)


def register_user(data):
    username = data['name']
    password = data['pwd']
    role = data['role']
    user_exist = r.get('username_' + username)
    if user_exist:
        return None
    r.set('username_' + username, password)
    return True


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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
    
    role = SelectField(u'Role', choices=[('user', 'user'), ('PI', 'PI')])


@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    print(user)
    logout_link = '<a href="/logout">log out</a>'
    return "Dashboard. [" + user.username + "] " + logout_link

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
"""

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="GET":
        form = LoginForm()
        return render_template("login.html",form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            user = auth_user(form.data)
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
    return redirect(url_for('login'))


@app.route('/register',methods=["GET","POST"])
def signup():
    if request.method =="GET":
        form = SignupForm()
        return render_template("register.html",form=form)
    else:
        form = SignupForm(formdata=request.form)
        if form.validate():
            user = register_user(form.data)
            if user:
                flask.flash('Register successful. Please login now.')
                return redirect(url_for('login'))
            else:
                print('failed.')
                flask.flash('Username exist.')
        else:
            print(form.errors, "signup error")
        return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
