import os
import time
import hashlib
import config
import math
from get_pair_file import generate_pair_file, generate_fake_file
from blocking import generate_pair_by_blocking, update_result_to_intfile
import blocking


def save_project(mongo, data):
    project_name = data['project_name']
    project_des = data['project_des']
    owner = data['owner']

    if 'pair_file' in data:
        pair_file = data['pair_file']
        file1 = data['file1']
        file2 = data['file2']

        pair_file.save(os.path.join(config.DATA_DIR, owner+'_'+project_name+'_pairfile.csv'))
        file1.save(os.path.join(config.DATA_DIR, owner+'_'+project_name+'_file1.csv'))
        file2.save(os.path.join(config.DATA_DIR, owner+'_'+project_name+'_file2.csv'))

        file_info = generate_pair_file(os.path.join(config.DATA_DIR, owner+'_'+project_name+'_pairfile.csv'), 
            os.path.join(config.DATA_DIR, owner+'_'+project_name+'_file1.csv'),
            os.path.join(config.DATA_DIR, owner+'_'+project_name+'_file2.csv'),
            os.path.join(config.DATA_DIR, owner+'_'+project_name+'_pf.csv'))

        
        
        # stub generate fake pair file
        #generate_fake_file(os.path.join(config.DATA_DIR, owner+'_'+project_name+'_pf.csv'))

    assignee = data['assignto']
    kapr = data['kapr']

    project_key = owner+'-'+project_name+str(time.time())
    project_key = project_key.encode('utf-8')
    pid = hashlib.sha224(project_key).hexdigest()

    project_data = {
        'pid': pid,
        'project_name': project_name, 
        'project_des': project_des, 
        'owner': owner,
        'pf_path': os.path.join(config.DATA_DIR, owner+'_'+project_name+'_pf.csv'),
        'assignee': [assignee],
        'assignee_stat': [
            {'assignee': assignee, 'current_page': 0, 'page_size': file_info['size']/6, 'kapr_limit': kapr, 'current_kapr': 0}
        ]
    }
    mongo.db.projects.insert(project_data)

    return pid


def save_project2(mongo, data):
    project_name = data['project_name']
    project_des = data['project_des']
    owner = data['owner']

    # generate pair_file for record linkage
    file1_path = os.path.join(config.DATA_DIR, 'database', owner+'_'+project_name+'_file1.csv')
    file2_path = os.path.join(config.DATA_DIR, 'database', owner+'_'+project_name+'_file2.csv')
    intfile_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_intfile.csv')
    pairfile_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_pairfile.csv')
    target_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_pf.csv')
    file1 = data['file1']
    file2 = data['file2']
    file1.save(file1_path)
    file2.save(file2_path)
    blocking_result = generate_pair_by_blocking(blocking=data['blocking'], file1=file1_path, file2=file2_path, intfile=intfile_path, pair_file=pairfile_path)
    # if blocking_result is False, need to consider this
    file_info = generate_pair_file(pairfile_path, file1_path, file2_path, target_path)

    assignee = data['assignto']
    kapr = data['kapr']

    project_key = owner+'-'+project_name+str(time.time())
    project_key = project_key.encode('utf-8')
    pid = hashlib.sha224(project_key).hexdigest()

    project_data = {
        'pid': pid,
        'project_name': project_name, 
        'project_des': project_des, 
        'owner': owner,
        'file1_path': file1_path,
        'file2_path': file2_path,
        'intfile_path': intfile_path,
        'pairfile_path': pairfile_path,
        'pf_path': target_path,
        'assignee': [assignee],
        'assignee_stat': [
            {'assignee': assignee, 'current_page': 0, 'page_size': math.ceil(file_info['size']/6), 'kapr_limit': kapr, 'current_kapr': 0}
        ]
    }
    mongo.db.projects.insert(project_data)

    return pid


def delete_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print(e)


def delete_project(mongo, pid, username):
    # delete related files
    project = mongo.db.projects.find_one({'pid': pid})
    file1_path = project['file1_path']
    file2_path = project['file2_path']
    pairfile_path = project['pairfile_path']
    pf_path = project['pf_path']
    delete_file(file1_path)
    delete_file(file2_path)
    delete_file(pairfile_path)
    delete_file(pf_path)

    ret = mongo.db.projects.delete_one({'pid': pid})
    return ret


def get_projects_by_owner(mongo, owner):
    projects = mongo.db.projects.find({'owner': owner})
    return projects


def get_project_by_pid(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    return project


def get_projects_assigned(mongo, user):
    assignments = mongo.db.projects.find({'assignee': [user]})
    return assignments


def get_assignment(mongo, username, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    return project


def get_assignment_status(mongo, username, pid):
    """
    assignment status = 
    {
        'current_page': 1,
        'page_size': 6
    }
    """
    assignment = mongo.db.projects.find_one({'pid': pid})

    assignee_stat = assignment['assignee_stat']
    user_idx = 0
    while user_idx < len(assignee_stat) and assignee_stat[user_idx]['assignee'] != username:
        user_idx += 1
    if user_idx == len(assignee_stat):
        print("error: cannot find user as assignee in this project, pid: %s, username: %s" % (pid, username))
    current_page = assignee_stat[user_idx]['current_page']
    page_size = assignee_stat[user_idx]['page_size']
    kapr_limit = assignee_stat[user_idx]['kapr_limit']
    current_kapr = assignee_stat[user_idx]['current_kapr']

    ret = {
        'current_page': int(current_page),
        'page_size': int(page_size),
        'kapr_limit': kapr_limit,
        'current_kapr': current_kapr
    }

    return ret


def increase_assignment_page(mongo, username, pid):
    assignment = mongo.db.projects.find_one({'pid': pid})
    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": username}, {"$inc": {"assignee_stat.$.current_page": 1}})


def update_kapr(mongo, username, pid, kapr):
    assignment = mongo.db.projects.find_one({'pid': pid})
    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": username}, {"$set": {"assignee_stat.$.current_kapr": kapr}})


def get_data_mode(assignment_id, ids, r):
    mode_dict = {'M': 'masked', 'P': 'partial', 'F': 'full'}
    data_mode_list = []

    for (id1, id2) in ids:
        cur_list = []
        for attribute_id1 in id1:
            key = assignment_id + '-' + attribute_id1
            mode = r.get(key)
            if mode != None:
                cur_list.append(mode_dict[mode])
            else:
                r.set(key, 'M')
                cur_list.append('masked')
        data_mode_list.append(cur_list)

    return data_mode_list


def get_pair_datafile(mongo, user, pid):
    assignment = mongo.db.projects.find_one({'pid': pid})
    pf_path = assignment['pf_path']
    return pf_path


def get_all_users(mongo):
    users = mongo.db.users.find()
    return users


def save_working_answers(assignment_id, data, r):
    """
    save answered responses to redis
    data: string
    """
    answers = list()
    for d in data:
        if d['type'] == 'final_answer':
            answers.append(d['value'])

    working_answers = ','.join(answers)

    key = assignment_id + '-working_answers'
    r.delete(key)
    r.set(key, working_answers)

    return True


def get_working_answers(assignment_id, r):
    key = assignment_id + '-working_answers'
    answers = r.get(key)
    if not answers:
        return []
    return answers.split(',')


def clear_working_page_cache(assignment_id, r):
    for key in r.scan_iter(assignment_id+"*"):
        r.delete(key)


def save_answers(pid, data):
    """
    save one page answers to file
    """
    data_to_write = list()
    print(data)
    for d in data:
        if d['type'] == 'final_answer':
            answer = d['value']
            pair_num = int(answer.split('a')[0][1:])
            choice = int(answer.split('a')[1])
            decision = 1 if choice > 3 else 0
            line = ','.join([str(pair_num), str(decision), str(choice)])
            data_to_write.append(line)

    filename = os.path.join('data', 'result', pid+'.csv')
    with open(filename, 'a') as f:
        for item in data_to_write:
            f.write(item + '\n')

    return True


def is_project_completed(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})

    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        if int(assignee['current_page']) < int(assignee['page_size']):
            return False
    return True


def update_project_setting(mongo, user, data):
    pid = data['pid']
    project_name = data['project_name']
    project_des = data['project_des']
    assignee = data['assignee']
    kapr_limit = data['kapr_limit']

    mongo.db.projects.update( {"pid": pid}, {"$set": {"project_name": project_name, "project_des": project_des}})

    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": assignee}, {"$set": {"assignee_stat.$.kapr_limit": float(kapr_limit)}})

    return True


def project_name_existed(mongo, data):
    project_name = data['project_name']
    owner = data['owner']
    existed = mongo.db.projects.find_one({'owner': owner, 'project_name': project_name})
    if existed:
        return True
    return False


def is_invalid_kapr(mongo, data):
    project = mongo.db.projects.find_one({'pid': data['pid']})

    assignee_stat = project['assignee_stat']
    user_idx = 0
    current_kapr = assignee_stat[user_idx]['current_kapr']

    if 100*float(current_kapr) > float(data['kapr_limit']):
        return True
    return False


def get_current_kapr(mongo, data):
    project = mongo.db.projects.find_one({'pid': data['pid']})

    assignee_stat = project['assignee_stat']
    user_idx = 0
    current_kapr = assignee_stat[user_idx]['current_kapr']

    current_kapr = round(100*float(current_kapr), 2)

    return current_kapr


def update_result(mongo, pid):
    result_file = os.path.join('data', 'result', pid+'.csv')
    project = mongo.db.projects.find_one({'pid': pid})
    pairfile_path = project['pairfile_path']
    intfile_path = project['intfile_path']

    update_result_to_intfile(result_file, pairfile_path, intfile_path)

    # reset result file
    with open(result_file, 'w+') as fout:
        fout.write('')


def new_blocking(mongo, data):
    project = mongo.db.projects.find_one({'pid': data['pid']})
    pid=data['pid']
    owner = project['owner']
    assignee = project['assignee'][0]
    file1_path = project['file1_path']
    file2_path = project['file2_path']
    intfile_path = project['intfile_path']
    pairfile_path = project['pairfile_path']
    target_path = project['pf_path']

    blocking_result = blocking.new_blocking(blocking=data['blocking'], intfile=intfile_path, pair_file=pairfile_path)
    if not blocking_result:
        return False

    file_info = generate_pair_file(pairfile_path, file1_path, file2_path, target_path)

    mongo.db.projects.update({"pid": pid, "assignee_stat.assignee": assignee}, {"$set": {"assignee_stat.$.current_page": 0}})
    mongo.db.projects.update({"pid": pid, "assignee_stat.assignee": assignee}, {"$set": {"assignee_stat.$.page_size": math.ceil(file_info['size']/6)}})
    mongo.db.projects.update({"pid": pid, "assignee_stat.assignee": assignee}, {"$set": {"assignee_stat.$.current_kapr": 0}})

    return pid


def mlog(mongo, data):
    mongo.db.log.insert(data)



