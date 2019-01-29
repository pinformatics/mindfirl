import flask
from flask import Flask, render_template, redirect, url_for, session, jsonify, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import redis
from wtforms.fields import SelectField, FileField, FloatField, SelectMultipleField, TextAreaField
from wtforms.fields import core, html5, simple
from wtforms import Form, validators, widgets
from urllib.parse import urlparse, urljoin
import os
import time
import json
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

#CORS(app) # very important!

if 'DYNO' in os.environ:
    # 1. Create new project in heroku. 
    # 2. Add Heroku Redis extension
    # 3. Add mLabMongoDB extension
    # 4. Click on the extension link in the project dashboard. It will take you to the mongo DB sandbox page
    # 5. Go to users and create a new user (eg: John) and password (eg: Abcd1234)
    # 6. Copy the mongo db uri they provide. It will look something like this: 
    #     mongodb://<dbuser>:<dbpassword>@df784663.mlab.com:47668/heroku_xxxx
    # 7. Replace the user and password with what you just created: mongodb://John:Abcd1234>@df784663.mlab.com:47668/heroku_xxxx
    # 8. Use this link as your mongodb uri in the application you push to Heroku. 
    app.config['MONGO_URI'] = 'mongodb://ilangurudev:2Hessian!@ds147668.mlab.com:47668/heroku_mqrk2vwm'
else:
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

    data1 = FileField(u'Data File 1 (csv)', render_kw={"class":"custom-file-input"}, validators=[validators.Optional()])
    data2 = FileField(u'Data File 2 (csv)', render_kw={"class":"custom-file-input"}, validators=[validators.Optional()])
    data3 = FileField(u'Paired data file (csv)', render_kw={"class":"custom-file-input"}, validators=[validators.Optional()])

    assignee_area = TextAreaField(u'Assignee', [validators.optional(), validators.length(max=200)], render_kw={"class":"form-control", "id": "assignee_area"})


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

    data1 = FileField(u'Data File 1 (csv)', render_kw={"class":"custom-file-input"}, validators=[validators.Optional()])
    data2 = FileField(u'Data File 2 (csv)', render_kw={"class":"custom-file-input"}, validators=[validators.Optional()])

    blocking_choices = [('id', 'ID'), ('fn', 'Firstname'), ('ln', 'Lastname'), ('bd', 'DoB'), ('gd', 'Gender'), ('rc', 'Race')]
    blocking = SelectMultipleField('Blocking', choices=blocking_choices, render_kw={"class":"form-control selectpicker"})

    '''
    assignto = SelectField(
        u'Assign to', 
        choices=[], 
        render_kw={"class":"form-control selectpicker", "data-live-search": "ture"}
    )
    kapr = FloatField('Privacy budget', [validators.NumberRange(min=0, max=100, message="Please enter a valid value.")], render_kw={"class":"form-control"})
    '''

    assignee_area = TextAreaField(u'Assignee', [validators.optional(), validators.length(max=200)], render_kw={"class":"form-control", "id": "assignee_area"})


class BlockForm(Form):
    blocking_choices = [('id', 'ID'), ('fn', 'Firstname'), ('ln', 'Lastname'), ('bd', 'DoB'), ('gd', 'Gender'), ('rc', 'Race')]
    blocking = SelectMultipleField('Blocking', choices=blocking_choices, render_kw={"class":"form-control selectpicker"})

    assignee_area = TextAreaField(u'Assignee', [validators.optional(), validators.length(max=200)], render_kw={"class":"form-control", "id": "assignee_area"})


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
                flask.flash('Incorrect username or password. Please try again.', 'alert-danger')
        else:
            print(form.errors, "login error")
        return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flask.flash('Logged out successfully.', 'alert-success')
    return redirect(url_for('login'))


@app.route('/register',methods=["GET","POST"])
def signup():
    if request.method =="GET":
        form = SignupForm()
        return render_template("register.html",form=form)
    else:
        form = SignupForm(formdata=request.form)
        if form.validate():
            data = form.data
            if data['name'] == data['pwd']:
                flask.flash('Cannot use username as password.', 'alert-danger')
                return redirect(url_for('signup'))
            user = register_user(mongo=mongo, data=form.data)
            if user:
                flask.flash('Register successful. Please login now.', 'alert-success')
                return redirect(url_for('login'))
            else:
                print('failed.')
                flask.flash('Username exist.', 'alert-danger')
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
        pair_idx, total_pairs = 0, 0
        for assignee in assignee_stat:
            pair_idx += int(assignee['pair_idx'])
            total_pairs += int(assignee['total_pairs'])
        progress = float(pair_idx)/total_pairs
        progress = round(100*progress, 2)
        p['progress'] = progress

    assignments = storage_model.get_projects_assigned(mongo=mongo, user=user.username)
    assignments = list(assignments)
    for a in assignments:
        assignee_stat = a['assignee_stat']
        finished_page, total_page = 0, 0
        for assignee in assignee_stat:
            if assignee['assignee'] == user.username:
                pair_idx = int(assignee['pair_idx'])
                total_pairs = int(assignee['total_pairs'])
                progress = float(pair_idx)/total_pairs
                progress = round(100*progress, 2)
                a['progress'] = progress
                break

        kapr = round(100*float(assignee_stat[0]['current_kapr']), 1)
        a['budget'] = kapr

    data = {
        'projects': projects[:3],
        'assignments': assignments[:3]
    }
    return render_template("project.html", data=data)


@app.route('/project_list')
@login_required
def project_list():
    user = current_user
    projects = storage_model.get_projects_by_owner(mongo=mongo, owner=user.username)
    projects = list(projects)

    # calculate projects progress
    for p in projects:
        assignee_stat = p['assignee_stat']
        pair_idx, total_pairs = 0, 0
        for assignee in assignee_stat:
            pair_idx += int(assignee['pair_idx'])
            total_pairs += int(assignee['total_pairs'])
        progress = float(pair_idx)/total_pairs
        progress = round(100*progress, 2)
        p['progress'] = progress

    data = {
        'projects': projects,
    }
    return render_template("project_list.html", data=data)


@app.route('/assignment_list')
@login_required
def assignment_list():
    user = current_user

    assignments = storage_model.get_projects_assigned(mongo=mongo, user=user.username)
    assignments = list(assignments)
    for a in assignments:
        assignee_stat = a['assignee_stat']

        for assignee in assignee_stat:
            if assignee['assignee'] == user.username:
                pair_idx = int(assignee['pair_idx'])
                total_pairs = int(assignee['total_pairs'])
                progress = float(pair_idx)/total_pairs
                progress = round(100*progress, 2)
                kapr = round(100*float(assignee['current_kapr']), 1)
                break
        a['progress'] = progress
        a['budget'] = kapr

    data = {
        'assignments': assignments
    }
    return render_template("assignment_list.html", data=data)


@app.route('/createProject')
@login_required
def create_project():
    form = ProjectForm()
    
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [u['username'] for u in all_users]
    data = {'users': user_list}

    return render_template("createProject.html", form=form, data=data)


@app.route('/createProject2')
@login_required
def create_project2():
    form = ProjectForm2()
    #all_users = storage_model.get_all_users(mongo=mongo)
    #user_list = [(u['username'], u['username']) for u in all_users]
    #form.assignto.choices = user_list

    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [u['username'] for u in all_users]
    data = {'users': user_list}
    return render_template("createProject2.html", form=form, data=data)


@app.route('/saveProject', methods=["POST"])
@login_required
def save_project():
    user = current_user
    form = ProjectForm(formdata=request.form)

    # because current software do not delete users, so no worry about different user list before and after
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [u['username'] for u in all_users]
    users = {'users': user_list}

    if form.validate():
        if 'data3' not in request.files or ('data1' not in request.files or 'data2' not in request.files):
            flask.flash('lack data files.', 'alert-danger')
            return render_template("createProject.html", form=form, data=users)

        data = form.data

        if 'data3' in request.files:
            pair_file = request.files['data3']
            data['pair_file'] = pair_file
            
            file1 = request.files['data1']
            file2 = request.files['data2']
            data['file1'] = file1
            data['file2'] = file2

        data['owner'] = user.username

        if storage_model.project_name_existed(mongo=mongo, data=data):
            flask.flash('project name existed. Please use another project name.', 'alert-danger')
            return render_template("createProject.html", form=form, data=users)

        pid = storage_model.save_project(mongo=mongo, data=data)

        # create result file
        filename = os.path.join(config.DATA_DIR, 'result', pid+'.csv')
        f = open(filename, 'w+')
        f.close()

        return redirect(url_for('project'))
    else:
        print(form.errors, "project creating error")
    return render_template("createProject.html", form=form, data=users)


@app.route('/saveProject2', methods=["POST"])
@login_required
def save_project2():
    user = current_user
    form = ProjectForm2(formdata=request.form)

    # because current software do not delete users, so no worry about different user list before and after
    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [u['username'] for u in all_users]
    users = {'users': user_list}

    if form.validate():
        if 'data1' not in request.files or 'data2' not in request.files:
            flask.flash('lack data files.', 'alert-danger')
            return render_template("createProject2.html", form=form, data=users)

        data = form.data
        
        file1 = request.files['data1']
        file2 = request.files['data2']
        data['file1'] = file1
        data['file2'] = file2

        data['owner'] = user.username

        if storage_model.project_name_existed(mongo=mongo, data=data):
            flask.flash('project name existed.', 'alert-danger')
            return render_template("createProject2.html", form=form, data=users)

        pid = storage_model.save_project2(mongo=mongo, data=data)

        return redirect(url_for('project'))
    else:
        print(form.errors, "project creating error")

    return render_template("createProject2.html", form=form, data=users)


@app.route('/project/<pid>')
@login_required
def project_detail(pid):
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    assignee_stat = project['assignee_stat']
    pair_idx, total_pairs = 0, 0
    for assignee in assignee_stat:
        pair_idx += int(assignee['pair_idx'])
        total_pairs += int(assignee['total_pairs'])
        assignee_progress = int(assignee['pair_idx'])/int(assignee['total_pairs'])
        assignee_progress = round(100*assignee_progress, 2)
        assignee['progress'] = assignee_progress
    progress = float(pair_idx)/total_pairs
    progress = round(100*progress, 2)
    project['progress'] = progress

    indices = storage_model.detect_result_conflicts(mongo, pid)
    if len(indices) > 0:
        project['conflicts'] = 1
    else:
        project['conflicts'] = 0

    print(project)

    data = {
        'project': project
    }

    return render_template('project_detail.html', data=data)


@app.route('/assignment/<pid>')
@login_required
def assignment_detail(pid):
    user = current_user
    assignment = storage_model.get_assignment(mongo=mongo, username=user.username, pid=pid)
    if not assignment:
        return page_not_found('page_not_found')

    assignee_stat = assignment['assignee_stat']

    for assignee in assignee_stat:
        if assignee['assignee'] == user.username:
            pair_idx = int(assignee['pair_idx'])
            total_pairs = int(assignee['total_pairs'])
            progress = float(pair_idx)/total_pairs
            progress = round(100*progress, 2)
            kapr = round(100*float(assignee['current_kapr']), 1)
            break
    assignment['progress'] = progress
    assignment['budget'] = kapr

    data = {
        'assignment': assignment
    }

    return render_template('assignment_detail.html', data=data)


@app.route('/delete/<pid>')
@login_required
def delete_project(pid):
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    storage_model.delete_project(mongo=mongo, pid=pid, username=user.username)

    flask.flash('Project has been deleted.', 'alert-success')

    return redirect('/project_list')


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
    #assignee = request.form['assignto']
    #kapr_limit = request.form['privacy_budget']

    data = {
        'pid': pid,
        'project_name': project_name,
        'project_des': project_des,
        #'assignee': assignee,
        #'kapr_limit': kapr_limit,
        'owner': user.username
    }

    # check if project name existed
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if project['project_name'] != data['project_name']:
        if storage_model.project_name_existed(mongo=mongo, data=data):
            flask.flash('project name existed.', 'alert-danger')
            return redirect(url_for('view_project', pid=pid))

    #if storage_model.is_invalid_kapr(mongo=mongo, data=data):
    #    current_kapr = storage_model.get_current_kapr(mongo=mongo, data=data)
    #    flask.flash('Kapr value is lower than the amount it has been used (%s%%).' % str(current_kapr), 'alert-danger')
    #    return redirect(url_for('view_project', pid=pid))

    storage_model.update_project_setting(mongo=mongo, user=user.username, data=data)

    flask.flash('Project update has been saved.', 'alert-success')
    return redirect(url_for('project'))


@app.route('/new_blocking/<pid>')
@login_required
def new_blocking(pid):
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    all_users = storage_model.get_all_users(mongo=mongo)
    user_list = [u['username'] for u in all_users]

    data = {
        'project': project,
        'users': user_list
    }

    form = BlockForm()

    return render_template('newBlocking.html', data=data, form=form)


@app.route('/new_blocking_save/<pid>', methods=["POST"])
@login_required
def new_blocking_save(pid):
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    form = BlockForm(formdata=request.form)

    if form.validate():
        data = form.data
        data['pid'] = pid
        data['owner'] = project['owner']
        data['project_name'] = project['project_name']
        result = storage_model.new_blocking(mongo=mongo, data=data)

        if not result:
            flask.flash('You have finished. No more blocking needed.', 'alert-success')
        else:
            flask.flash('New blocking has been processed.', 'alert-success')
    else:
        print(form.errors, "new blocking error")
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

    # get assignment status
    assignment_status = storage_model.get_assignment_status(mongo=mongo, username=user.username, pid=pid)
    current_page = assignment_status['current_page']
    page_size = assignment_status['page_size']
    kapr_limit = assignment_status['kapr_limit']
    current_kapr = assignment_status['current_kapr']
    if current_page >= page_size:
        flask.flash('You have completed the project.', 'alert-success')
        return redirect('project')

    # get working data and full data
    pair_datafile = storage_model.get_pair_datafile(mongo=mongo, user=user, pid=pid)
    indices, pair_idx = storage_model.get_current_block(mongo=mongo, pid=pid, assignee=user.username)
    working_data = dm.DataPairList(data_pairs=dl.load_data_from_csv(pair_datafile), indices=indices)
    full_data = dl.load_data_from_csv(pair_datafile)

    # prepare return data
    icons = working_data.get_icons()
    ids_list = working_data.get_ids()
    ids = list(zip(ids_list[0::2], ids_list[1::2]))
    data_mode = 'masked'
    data_mode_list = storage_model.get_data_mode(assignment_id, ids, r=r)
    pairs_formatted = working_data.get_data_display(data_mode, data_mode_list)
    data = list(zip(pairs_formatted[0::2], pairs_formatted[1::2]))

    # get the delta information
    delta = list()
    for i in range(working_data.size()):
        data_pair = working_data.get_data_pair_by_index(i)
        if data_pair is None:
            break
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
        'pair_num_base': pair_idx+1,
        'delta': delta,
        'this_url': '/record_linkage/'+pid,
        'saved_answers': answers,
        'data_size': len(data),
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

    # increase pair index to db
    storage_model.increase_pair_idx(mongo=mongo, pid=pid, username=user.username)

    # update kapr to db
    KAPR_key = assignment_id + '_KAPR'
    kapr = r.get(KAPR_key)
    storage_model.update_kapr(mongo=mongo, username=user.username, pid=pid, kapr=kapr)

    # flush related cache in redis
    storage_model.clear_working_page_cache(assignment_id, r)

    # check if the project is completed
    completed = storage_model.is_project_completed(mongo=mongo, pid=pid)
    if completed:
        storage_model.combine_result(mongo, pid)
        # don't update the result yet, because we use ajax to write result, the result might not been updated 
        # if there are conflicts, the result is updated after the resolve_conflict
        indices = storage_model.detect_result_conflicts(mongo, pid)
        if len(indices) == 0:
            storage_model.update_result(mongo=mongo, pid=pid)

        flask.flash('You have completed the project.', 'alert-success')
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

    log_data = {
        'username': user.username,
        'timestamp': time.time(),
        'url': '/get_cell',
        'pid': str(pid),
        'assignment_id': str(assignment_id),
        'log': json.dumps(ret)
    }
    storage_model.mlog(mongo=mongo, data=log_data)

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

    log_data = {
        'username': user.username,
        'timestamp': time.time(),
        'url': '/get_big_cell',
        'pid': str(pid),
        'assignment_id': str(assignment_id),
        'log': json.dumps(ret)
    }
    storage_model.mlog(mongo=mongo, data=log_data)

    return jsonify(ret)


@app.route('/resolve_conflicts/<pid>')
@login_required
def resolve_conflicts(pid):
    user = current_user
    assignment_id = pid + '-' + user.username

    # find if this project exist
    project = storage_model.get_assignment(mongo=mongo, username=user.username, pid=pid)
    if not project:
        return page_not_found('page_not_found')

    indices = storage_model.detect_result_conflicts(mongo, pid)
    pair_datafile = storage_model.get_pair_datafile(mongo=mongo, user=user, pid=pid)
    working_data = dm.DataPairList(data_pairs=dl.load_data_from_csv(pair_datafile), indices=indices)

    icons = working_data.get_icons()
    ids_list = working_data.get_ids()
    ids = list(zip(ids_list[0::2], ids_list[1::2]))
    
    pairs_formatted = working_data.get_data_display('full')
    data = list(zip(pairs_formatted[0::2], pairs_formatted[1::2]))


    ret_data = {
        'data': data,
        'icons': icons,
        'ids': ids,
        'title': project['project_name'],
        'this_url': '/record_linkage/'+pid,
        'next_url': '/project/'+pid,
        'pid': pid,
        'data_size': len(data),
    }
    return render_template('resolve_conflicts.html', data=ret_data)


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

    storage_model.save_answers(mongo, pid, user.username, formatted_data)

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


@app.route('/save_data_resolve_conflicts/<pid>', methods=['GET', 'POST'])
@login_required
def save_data_resolve_conflicts(pid):
    user = current_user

    user_data_raw = request.form['user_data']
    data_list = user_data_raw.split(';')
    user_data = ''
    for line in data_list:
        if line:
            user_data += ('uid:'+user.username+','+line+';')
    formatted_data = ud.parse_user_data(user_data)

    storage_model.save_resolve_conflicts(mongo, pid, user.username, formatted_data)

    storage_model.update_result(mongo=mongo, pid=pid)

    return 'data_saved.'


@app.route('/get_result/<pid>')
@login_required
def get_file(pid):
    """Download a file."""
    user = current_user
    project = storage_model.get_project_by_pid(mongo=mongo, pid=pid)
    if not project:
        return page_not_found('page_not_found')
    if project['owner'] != user.username:
        return forbidden()

    path = storage_model.get_result_path(mongo=mongo, pid=pid)
    return send_from_directory('', path, as_attachment=True, attachment_filename='result.csv')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html')



