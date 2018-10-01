import flask
from flask import Flask, render_template, redirect, url_for, session, jsonify, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import redis
from wtforms.fields import SelectField, FileField, FloatField, SelectMultipleField
from wtforms.fields import core, html5, simple
from wtforms import Form, validators, widgets
from urllib.parse import urlparse, urljoin
import os
from user import User, auth_user, register_user
from mutil import r
from flask_pymongo import PyMongo
import storage_model
import data_model as dm
import data_loader as dl
import user_data as ud
import config


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


class ProjectForm(Form):
    project_name = simple.StringField(
        label="Project name",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="project name cannot be empty"),
            validators.Length(max=50,min=1,message="The length of username should between 1 and 50"),
            validators.Regexp('^[a-zA-Z0-9_.-]*$', flags=0, message="must be characters or digits only.")
        ],
        render_kw={"class":"form-control"}
    )

    project_des = simple.StringField(
        label="Project description (optional)",
        widget=widgets.TextInput(),
        validators=[
            validators.Length(max=50,min=0,message="The length of username should between 0 and 50")
        ],
        render_kw={"class":"form-control"}
    )

    data1 = FileField(u'Data File 1 (csv)', render_kw={"class":"form-control-file"}, validators=[validators.Optional()])
    data2 = FileField(u'Data File 2 (csv)', render_kw={"class":"form-control-file"}, validators=[validators.Optional()])

    data3 = FileField(u'Paired data file (csv)', render_kw={"class":"form-control-file"}, validators=[validators.Optional()])

    assignto = SelectField(
        u'Assign to', 
        choices=[], 
        render_kw={"class":"custom-select my-1 mr-sm-2"}
    )
    kapr = FloatField('Privacy budget', [validators.NumberRange(min=0, max=100)], render_kw={"class":"form-control"})


class ProjectForm2(Form):
    project_name = simple.StringField(
        label="Project name",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="project name cannot be empty"),
            validators.Length(max=50,min=1,message="The length of username should between 1 and 50"),
            validators.Regexp('^[a-zA-Z0-9_.-]*$', flags=0, message="must be characters or digits only.")
        ],
        render_kw={"class":"form-control"}
    )

    project_des = simple.StringField(
        label="Project description (optional)",
        widget=widgets.TextInput(),
        validators=[
            validators.Length(max=50,min=0,message="The length of username should between 0 and 50")
        ],
        render_kw={"class":"form-control"}
    )

    data1 = FileField(u'Data File 1 (csv)', render_kw={"class":"form-control-file"}, validators=[validators.Optional()])
    data2 = FileField(u'Data File 2 (csv)', render_kw={"class":"form-control-file"}, validators=[validators.Optional()])

    blocking_choices = [('id', 'ID'), ('fn', 'Firstname'), ('ln', 'Lastname'), ('bd', 'DoB'), ('gd', 'Gender'), ('rc', 'Race')]
    blocking = SelectMultipleField('Blocking', choices=blocking_choices, render_kw={"class":"form-control"})

    assignto = SelectField(
        u'Assign to', 
        choices=[], 
        render_kw={"class":"custom-select my-1 mr-sm-2"}
    )
    kapr = FloatField('Privacy budget', [validators.NumberRange(min=0, max=100, message="Please enter a valid value.")], render_kw={"class":"form-control"})


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


@app.route("/")
@app.route("/index")
def index():
    return redirect(url_for('project'))


@app.route('/project')
@login_required
def project():
    user = current_user
    projects = storage_model.get_projects_by_owner(mongo=mongo, owner=user.username)
    projects = list(projects)

    # calculate projects progress
    for p in projects:
        assignee_stat = p['assignee_stat']
        finished_page, total_page = 0, 0
        for assignee in assignee_stat:
            finished_page += int(assignee['current_page'])
            total_page += int(assignee['page_size'])
        progress = float(finished_page)/total_page
        progress = round(100*progress, 2)
        p['progress'] = progress

    assignments = storage_model.get_projects_assigned(mongo=mongo, user=user.username)
    assignments = list(assignments)
    for a in assignments:
        assignee_stat = a['assignee_stat']
        finished_page, total_page = 0, 0
        for assignee in assignee_stat:
            finished_page += int(assignee['current_page'])
            total_page += int(assignee['page_size'])
        progress = float(finished_page)/total_page
        progress = round(100*progress, 2)
        a['progress'] = progress

        kapr = round(100*float(assignee_stat[0]['current_kapr']), 1)
        a['budget'] = kapr

    data = {
        'projects': projects,
        'assignments': assignments
    }
    return render_template("project.html", data=data)


@app.route('/createProject')
@login_required
def create_project():
    form = ProjectForm()
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [(u['username'], u['username']) for u in all_users]
    form.assignto.choices = user_list
    return render_template("createProject.html", form=form)


@app.route('/createProject2')
@login_required
def create_project2():
    form = ProjectForm2()
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [(u['username'], u['username']) for u in all_users]
    form.assignto.choices = user_list
    return render_template("createProject2.html", form=form)


@app.route('/saveProject', methods=["POST"])
@login_required
def save_project():
    user = current_user
    form = ProjectForm(formdata=request.form)

    # because current software do not delete users, so no worry about different user list before and after
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [(u['username'], u['username']) for u in all_users]
    form.assignto.choices = user_list

    if form.validate():
        if 'data3' not in request.files or ('data1' not in request.files or 'data2' not in request.files):
            flask.flash('lack data files.')
            return render_template("createProject.html", form=form)

        data = form.data

        if 'data3' in request.files:
            pair_file = request.files['data3']
            data['pair_file'] = pair_file
            
            file1 = request.files['data1']
            file2 = request.files['data2']
            data['file1'] = file1
            data['file2'] = file2

        data['owner'] = user.username

        pid = storage_model.save_project(mongo=mongo, data=data)

        # create result file
        filename = os.path.join(config.DATA_DIR, 'result', pid+'.csv')
        f = open(filename, 'w+')
        f.close()

        return redirect(url_for('project'))
    else:
        print(form.errors, "project creating error")
    return render_template("createProject.html", form=form)


@app.route('/saveProject2', methods=["POST"])
@login_required
def save_project2():
    user = current_user
    form = ProjectForm2(formdata=request.form)

    # because current software do not delete users, so no worry about different user list before and after
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [(u['username'], u['username']) for u in all_users]
    form.assignto.choices = user_list

    if form.validate():
        if 'data1' not in request.files or 'data2' not in request.files:
            flask.flash('lack data files.')
            return render_template("createProject2.html", form=form)

        data = form.data
        
        file1 = request.files['data1']
        file2 = request.files['data2']
        data['file1'] = file1
        data['file2'] = file2

        data['owner'] = user.username

        if storage_model.project_name_existed(mongo=mongo, data=data):
            flask.flash('project name existed.')
            return render_template("createProject2.html", form=form)

        pid = storage_model.save_project2(mongo=mongo, data=data)

        # create result file
        filename = os.path.join(config.DATA_DIR, 'result', pid+'.csv')
        f = open(filename, 'w+')
        f.close()

        return redirect(url_for('project'))
    else:
        print(form.errors, "project creating error")
    return render_template("createProject2.html", form=form)


@app.route('/delete/<pid>')
@login_required
def delete_project(pid):
    user = current_user

    storage_model.delete_project(mongo=mongo, pid=pid, username=user.username)

    return redirect('/project')


@app.route('/viewProjectConfig/<pid>')
@login_required
def view_project(pid):
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    data = {
        'project': project
    }

    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [(u['username'], u['username']) for u in all_users]

    return render_template('viewProject.html', data=data)


@app.route('/updateProject/<pid>', methods=["POST"])
@login_required
def update_project(pid):
    user = current_user

    project_name = request.form['project_name']
    project_des = request.form['project_description']
    assignee = request.form['assignto']
    kapr_limit = request.form['privacy_budget']

    data = {
        'pid': pid,
        'project_name': project_name,
        'project_des': project_des,
        'assignee': assignee,
        'kapr_limit': kapr_limit
    }

    if storage_model.is_invalid_kapr(mongo=mongo, data=data):
        current_kapr = storage_model.get_current_kapr(mongo=mongo, data=data)
        flask.flash('Kapr value is lower than the amount it has been used (%s%%).' % str(current_kapr))
        return redirect(url_for('view_project', pid=pid))

    storage_model.update_project_setting(mongo=mongo, user=user.username, data=data)

    return redirect(url_for('project'))


@app.route('/guide')
@login_required
def guide():
    return render_template('help.html')


@app.route('/record_linkage/<pid>', methods=["GET"])
@login_required
def record_linkage(pid):
    user = current_user

    # find if this project exist
    project = storage_model.get_assignment(mongo=mongo, username=user.username, pid=pid)
    if not project:
        return page_not_found('page_not_found')

    # username and project_id can identify an assignment
    assignment_id = pid + '-' + user.username

    # get working data and full data
    pair_datafile = storage_model.get_pair_datafile(mongo=mongo, user=user, pid=pid)
    working_data = dm.DataPairList(data_pairs = dl.load_data_from_csv(pair_datafile))
    full_data = dl.load_data_from_csv(pair_datafile)

    # get assignment status
    assignment_status = storage_model.get_assignment_status(mongo=mongo, username=user.username, pid=pid)
    current_page = assignment_status['current_page']
    page_size = assignment_status['page_size']
    kapr_limit = assignment_status['kapr_limit']
    current_kapr = assignment_status['current_kapr']
    if current_page >= page_size:
        return redirect('project')

    # prepare return data
    icons = working_data.get_icons()[config.DATA_PAIR_PER_PAGE*current_page:config.DATA_PAIR_PER_PAGE*(current_page+1)]
    ids_list = working_data.get_ids()[2*config.DATA_PAIR_PER_PAGE*current_page:2*config.DATA_PAIR_PER_PAGE*(current_page+1)]
    ids = list(zip(ids_list[0::2], ids_list[1::2]))
    data_mode = 'masked'
    data_mode_list = storage_model.get_data_mode(assignment_id, ids, r=r)
    pairs_formatted = working_data.get_data_display(data_mode, data_mode_list, left=config.DATA_PAIR_PER_PAGE*current_page, right=config.DATA_PAIR_PER_PAGE*(current_page+1))
    data = list(zip(pairs_formatted[0::2], pairs_formatted[1::2]))

    # get the delta information
    delta = list()
    for i in range(config.DATA_PAIR_PER_PAGE*current_page, config.DATA_PAIR_PER_PAGE*(current_page+1)):
        data_pair = working_data.get_data_pair_by_index(i)
        delta += dm.KAPR_delta(full_data, data_pair, ['M', 'M', 'M', 'M', 'M', 'M'], 2*working_data.size())

    # prepare cache data for ajax query
    r.set(user.username+'_working_pid', pid)
    KAPR_key = assignment_id + '_KAPR'
    r.set(KAPR_key, float(current_kapr))

    # get saved working answers
    answers = storage_model.get_working_answers(assignment_id, r)

    ret_data = {
        'data': data,
        'icons': icons,
        'ids': ids,
        'title': project['project_name'],
        'kapr': round(100*float(current_kapr), 1),
        'kapr_limit': kapr_limit, 
        'page_number': current_page+1,
        'page_size': page_size,
        'pair_num_base': config.DATA_PAIR_PER_PAGE*current_page+1,
        'delta': delta,
        'this_url': '/record_linkage/'+pid,
        'saved_answers': answers
    }
    return render_template('record_linkage_ppirl.html', data=ret_data)


@app.route('/record_linkage/<pid>/next', methods=["GET"])
@login_required
def record_linkage_next(pid):
    """
    update page number to db
    update kapr to db
    flush related cache in redis
    """
    user = current_user
    assignment_id = pid + '-' + user.username

    # find if this project exist
    project = storage_model.get_assignment(mongo=mongo, username=user.username, pid=pid)
    if not project:
        return page_not_found('page_not_found')

    # increase page number to db
    storage_model.increase_assignment_page(mongo=mongo, username=user.username, pid=pid)

    # update kapr to db
    KAPR_key = assignment_id + '_KAPR'
    kapr = r.get(KAPR_key)
    storage_model.update_kapr(mongo=mongo, username=user.username, pid=pid, kapr=kapr)

    # flush related cache in redis
    storage_model.clear_working_page_cache(assignment_id, r)

    # check if the project is completed
    completed = storage_model.is_project_completed(mongo=mongo, pid=pid)
    if completed:
        return redirect('project')

    return redirect('record_linkage/'+pid)


@app.route('/get_cell', methods=['GET', 'POST'])
@login_required
def open_cell():
    user = current_user
    pid = r.get(user.username+'_working_pid')
    assignment_id = pid + '-' + user.username

    pair_datafile = storage_model.get_pair_datafile(mongo=mongo, user=user, pid=pid)
    full_data = dl.load_data_from_csv(pair_datafile)
    working_data = dm.DataPairList(data_pairs = dl.load_data_from_csv(pair_datafile))

    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    mode = request.args.get('mode')
    pair_num = str(id1.split('-')[0])
    attr_num = str(id1.split('-')[2])

    assignment_status = storage_model.get_assignment_status(mongo=mongo, username=user.username, pid=pid)
    kapr_limit = float(assignment_status['kapr_limit'])

    ret = dm.open_cell(assignment_id, full_data, working_data, pair_num, attr_num, mode, r, kapr_limit)
    return jsonify(ret)


@app.route('/get_big_cell', methods=['GET', 'POST'])
def open_big_cell():
    user = current_user
    pid = r.get(user.username+'_working_pid')
    assignment_id = pid + '-' + user.username

    pair_datafile = storage_model.get_pair_datafile(mongo=mongo, user=user, pid=pid)
    full_data = dl.load_data_from_csv(pair_datafile)
    working_data = dm.DataPairList(data_pairs = dl.load_data_from_csv(pair_datafile))
    assignment_status = storage_model.get_assignment_status(mongo=mongo, username=user.username, pid=pid)
    kapr_limit = float(assignment_status['kapr_limit'])

    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    id3 = request.args.get('id3')
    id4 = request.args.get('id4')
    mode = request.args.get('mode')

    pair_num1 = str(id1.split('-')[0])
    attr_num1 = str(id1.split('-')[2])
    ret1 = dm.open_cell(assignment_id, full_data, working_data, pair_num1, attr_num1, mode, r, kapr_limit)
    pair_num2 = str(id3.split('-')[0])
    attr_num2 = str(id3.split('-')[2])
    ret2 = dm.open_cell(assignment_id, full_data, working_data, pair_num2, attr_num2, mode, r, kapr_limit)

    if ret2['result'] == 'fail':
        return jsonify(ret2)

    ret = {
        'value1': ret1['value1'],
        'value2': ret1['value2'],
        'value3': ret2['value1'],
        'value4': ret2['value2'],
        'id': ret1['id'],
        'mode': ret2['mode'],
        'KAPR': ret2['KAPR'],
        'result': ret2['result'],
        'new_delta': ret2['new_delta']
    }

    return jsonify(ret)


@app.route('/save_data', methods=['GET', 'POST'])
@login_required
def save_data():
    user = current_user
    pid = r.get(user.username+'_working_pid')
    assignment_id = pid + '-' + user.username

    user_data_raw = request.form['user_data']
    data_list = user_data_raw.split(';')
    user_data = ''
    for line in data_list:
        if line:
            user_data += ('uid:'+user.username+','+line+';')
    formatted_data = ud.parse_user_data(user_data)

    storage_model.save_answers(pid, formatted_data)

    user_data_key = assignment_id + '_user_data'
    r.append(user_data_key, formatted_data)
    return 'data_saved.'


@app.route('/save_exit', methods=['POST'])
@login_required
def save_exit():
    """
    during record linkage, save and exit the current page
    1. save answered responses to redis
    2. save kapr to mongodb
    """
    user = current_user
    pid = r.get(user.username+'_working_pid')
    assignment_id = pid + '-' + user.username

    user_data_raw = request.form['user_data']
    data_list = user_data_raw.split(';')
    user_data = ''
    for line in data_list:
        if line:
            user_data += ('uid:'+user.username+','+line+';')
    formatted_data = ud.parse_user_data(user_data)
    
    storage_model.save_working_answers(assignment_id, formatted_data, r)

    # update kapr to db
    KAPR_key = assignment_id + '_KAPR'
    kapr = r.get(KAPR_key)
    storage_model.update_kapr(mongo=mongo, username=user.username, pid=pid, kapr=kapr)

    return "data saved."


@app.route('/get_result/<filename>')
@login_required
def get_file(filename):
    """Download a file."""
    user = current_user

    path = os.path.join('data', 'result', filename)
    return send_from_directory('', path, as_attachment=True)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html')



