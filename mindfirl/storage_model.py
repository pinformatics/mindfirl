import os
import time
import hashlib
import config
import math
from get_pair_file_extra import generate_pair_file
from get_pair_file_2_extra import generate_pair_file2
from blocking import generate_pair_by_blocking, update_result_to_intfile
import blocking
import numpy as np
from collections import defaultdict


class Assign_generator(object):
    def __init__(self, pair_file, block_id):
        # create a dict {id: line_num}
        self.line_dict = dict()
        with open(pair_file, 'r') as fin:
            self.lines = fin.readlines()
            for i in range(1, len(self.lines), 2):
                cur_id = int(self.lines[i].split(',')[0])
                self.line_dict[cur_id] = i

        self.block_id = block_id
        self.block_list = list(range(len(block_id)))
        np.random.shuffle(self.block_list)

        self.loc = 0
        self.size = len(self.block_list)
        self.block_list = self.block_list + self.block_list

    def random_assign(self, tmp_file, pair_num, block_id):
        selected = list()
        cnt = 0
        while(cnt < pair_num):
            # assign one block
            cur_block_id = self.block_list[self.loc]
            cur_block = self.block_id[cur_block_id]
            for pair_id in cur_block:
                selected.append(pair_id)
                cnt += 1
            self.loc += 1
            if self.loc >= self.size:
                self.loc = 0

        '''
        selected = self.idx[self.loc:self.loc+pair_num]
        if self.loc + pair_num >= self.size:
            self.loc = pair_num - (self.size - self.loc)
        else:
            self.loc = self.loc + pair_num
        '''
        selected.sort()

        data = list()
        data.append(self.lines[0])
        for cur_id in selected:
            line_num = self.line_dict[cur_id]
            data.append(self.lines[line_num])
            data.append(self.lines[line_num+1])

        with open(tmp_file, 'w+') as fout:
            for line in data:
                fout.write(line)

        # make assigned_id grouped in blocks
        grouped_assigned_id = list()
        for block in block_id:
            cur_block = list()
            for idx in selected:
                if idx in block:
                    cur_block.append(idx)
            if cur_block:
                grouped_assigned_id.append(cur_block)

        return grouped_assigned_id


def build_save_pairfile_3(pairfile_path, name_freq_file_path, internal_pairfile_path):
    """
    Please see MINDFIRL design document to see the format of input pairfile
    The MINDFIRL system internally need 3 files: a different pairfile, file1, and file2
    This function turn the input pairfile and name_freq_file into those 3 files
    """
    table_head = 'ID,voter_reg_num,first_name,last_name,dob,sex,race,info1,info2,info3,info4,info5,type,file_id\n'
    fout = open(internal_pairfile_path, 'w+')
    fout.write(table_head)

    pairfile = open(pairfile_path, 'r')
    cnt = 0
    for l in pairfile:
        if cnt != 0:
            l = l.strip().split(',')
            newline = [l[0], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12], l[13], l[14]]
            newline.append('1')
            if cnt%2 == 0:
                newline.append('1-A')
            else:
                newline.append('1-B')
            newline = ','.join(newline)
            fout.write(newline+'\n')
        cnt += 1

    fout.close()
    pairfile.close()


def get_blockid_from_pairfile(pairfile_path):
    cnt = 0
    data = list()
    with open(pairfile_path, 'r') as fin:
        for line in fin:
            if cnt != 0:
                line = line.strip().split(',')
                data.append([int(line[0]), int(line[1])])
            cnt += 1

    ret = list()
    group_id = 1
    while True:
        cur_group = list()
        for i in np.arange(0, len(data), 2):
            if data[i][1] == group_id:
                cur_group.append(data[i][0])

        # no more pairs for this group_id
        if len(cur_group) == 0:
            break

        ret.append(cur_group)

        group_id += 1

    return ret


def delete_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print(e)


def get_total_pairs_from_pairfile(pairfile):
    cnt = 0
    with open(pairfile, 'r') as fin:
        for line in fin:
            if len(line) > 0:
                cnt += 1

    return (cnt-1)/2

def get_blockid_from_groupfile(groupfile):
    block_id = list()
    with open(groupfile, 'r') as fin:
        for line in fin:
            data = line.rstrip().split(',')
            if len(data) > 0:
                data = [int(x) for x in data]
                block_id.append(data)
    return block_id

def get_block_num(block_id, pf_file):
    """
    get how many blocks exist in the pf_file
    """
    pair_id = list()

    with open(pf_file, 'r') as fin:
        for line in fin:
            data = line.rstrip().split(',')
            pair_id.append(int(data[0]))

    pair_num = 0
    for cur_block in block_id:
        flag = False
        for value in cur_block:
            if value in pair_id:
                flag = True
                break
        if flag:
            pair_num += 1

    return pair_num

def get_block_id_len(block_id):
    total = 0
    for i in block_id:
        total += len(i)
    return total

def save_project(mongo, data):
    project_name = data['project_name']
    project_des = data['project_des']
    owner = data['owner']

    pair_file = data['pair_file']
    name_freq_file = data['name_freq_file']

    pairfile_path = os.path.join(config.DATA_DIR, 'database', owner+'_'+project_name+'_pairfile.csv')
    name_freq_file_path = os.path.join(config.DATA_DIR, 'database', owner+'_'+project_name+'_freqfile.csv')
    internal_pairfile_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_pairfile.csv')
    pf_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_pf.csv')
    result_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_result.csv')
    final_result_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_finalresult.csv')

    # create result file
    f = open(result_path, 'w+')
    f.close()
    f = open(final_result_path, 'w+')
    f.close()

    pair_file.save(pairfile_path)
    name_freq_file.save(name_freq_file_path)
    build_save_pairfile_3(pairfile_path, name_freq_file_path, internal_pairfile_path)
    #pf_result = generate_pair_file2(internal_pairfile_path, name_freq_file_path, pf_path)
    pf_result = generate_pair_file(internal_pairfile_path, internal_pairfile_path, internal_pairfile_path, pf_path)

    total_pairs = get_total_pairs_from_pairfile(internal_pairfile_path)

    # get block_id
    #block_id = get_blockid_from_groupfile(groupfile_path)
    block_id = get_blockid_from_pairfile(pairfile_path)

    assigner = Assign_generator(internal_pairfile_path, block_id)
    assignee_items = data['assignee_area'].rstrip(';').split(';')
    assignee_list = list()
    assignee_stat = list()
    for assignee_item in assignee_items:
        cur_assignee, cur_kapr, cur_percentage, isfull = assignee_item.split(',')
        assignee_list.append(cur_assignee)

        percentage = float(cur_percentage)/100.0
        tmp_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+cur_assignee+'_'+project_name+'_pairfile.csv')
        #assigned_id = assigner.random_assign_pairfile(tmp_file=tmp_file, pair_num=int(total_pairs*percentage))
        assigned_id = assigner.random_assign(tmp_file=tmp_file, pair_num=math.ceil(total_pairs*percentage), block_id=block_id)
        pf_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_pf.csv')
        # TODO
        pf_result = generate_pair_file2(tmp_file, name_freq_file_path, pf_file)
        delete_file(tmp_file)

        total_blocks = get_block_num(block_id=block_id, pf_file=pf_file)

        # create assignee result file
        cur_result = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_result.csv')
        f = open(cur_result, 'w+')
        f.close()

        assignee_stat.append({
            'assignee': cur_assignee, 
            'pf_path': pf_file,
            'result_path': cur_result,
            'assigned_id': assigned_id,
            'current_page': 0, 
            #'page_size': math.ceil(int(total_pairs*percentage)/6), 
            'page_size': total_blocks, 
            'pair_idx': 0,
            'total_pairs': get_block_id_len(assigned_id),
            'kapr_limit': cur_kapr, 
            'isfull': isfull,
            'current_kapr': 0,
        })

    project_key = owner+'-'+project_name+str(time.time())
    project_key = project_key.encode('utf-8')
    pid = hashlib.sha224(project_key).hexdigest()

    project_data = {
        'pid': pid,
        'project_name': project_name, 
        'project_des': project_des, 
        'owner': owner,
        'created_by': 'pairfile',
        'pairfile_path': pairfile_path,
        'internal_pairfile_path': internal_pairfile_path,
        'pf_path': pf_path,
        'result_path': result_path,
        'final_result_path': final_result_path,
        'block_id': block_id,
        'assignee': assignee_list,
        'assignee_stat': assignee_stat
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
    pf_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_pf.csv')
    result_path = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_result.csv')
    file1 = data['file1']
    file2 = data['file2']
    file1.save(file1_path)
    file2.save(file2_path)

    total_pairs, block_id = generate_pair_by_blocking(blocking=data['blocking'], file1=file1_path, file2=file2_path, intfile=intfile_path, pair_file=pairfile_path)

    # if blocking_result is False, need to consider this
    pf_result = generate_pair_file(pairfile_path, file1_path, file2_path, pf_path)

    # create result file
    f = open(result_path, 'w+')
    f.close()

    # assign the pairfile to each assignee, generate pf_file for them
    assigner = Assign_generator(pairfile_path, block_id)
    assignee_items = data['assignee_area'].rstrip(';').split(';')
    assignee_list = list()
    assignee_stat = list()
    for assignee_item in assignee_items:
        cur_assignee, cur_kapr, cur_percentage, isfull = assignee_item.split(',')
        assignee_list.append(cur_assignee)

        percentage = float(cur_percentage)/100.0
        tmp_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+cur_assignee+'_'+project_name+'_pairfile.csv')
        assigned_id = assigner.random_assign(tmp_file=tmp_file, pair_num=math.ceil(total_pairs*percentage), block_id=block_id)
        pf_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_pf.csv')
        pf_result = generate_pair_file(tmp_file, file1_path, file2_path, pf_file)
        delete_file(tmp_file)

        total_blocks = get_block_num(block_id=block_id, pf_file=pf_file)

        # create assignee result file
        cur_result = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_result.csv')
        f = open(cur_result, 'w+')
        f.close()

        assignee_stat.append({
            'assignee': cur_assignee, 
            'pf_path': pf_file,
            'result_path': cur_result,
            'assigned_id': assigned_id,
            'current_page': 0, 
            'page_size': total_blocks, 
            'kapr_limit': cur_kapr, 
            'current_kapr': 0,
            'pair_idx': 0,
            'total_pairs': pf_result['size'],
            'isfull': isfull,
        })

    project_key = owner+'-'+project_name+str(time.time())
    project_key = project_key.encode('utf-8')
    pid = hashlib.sha224(project_key).hexdigest()

    project_data = {
        'pid': pid,
        'project_name': project_name, 
        'project_des': project_des, 
        'owner': owner,
        'created_by': 'blocking',
        'blocking_on': data['blocking'],
        'block_id': block_id,
        'file1_path': file1_path,
        'file2_path': file2_path,
        'intfile_path': intfile_path,
        'pairfile_path': pairfile_path,
        'pf_path': pf_path,
        'result_path': result_path,
        'assignee': assignee_list,
        'assignee_stat': assignee_stat
    }
    mongo.db.projects.insert(project_data)

    return pid


def delete_project(mongo, pid, username):
    # delete related files
    project = mongo.db.projects.find_one({'pid': pid})

    if 'intfile_path' in project:
        intfile_path = project['intfile_path']
        delete_file(intfile_path)
    pairfile_path = project['pairfile_path']
    result_path = project['result_path']

    delete_file(pairfile_path)
    delete_file(result_path)

    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        pf_path = assignee['pf_path']
        result_path = assignee['result_path']
        delete_file(pf_path)
        delete_file(result_path)

    ret = mongo.db.projects.delete_one({'pid': pid})
    return ret


def get_projects_by_owner(mongo, owner):
    projects = mongo.db.projects.find({'owner': owner})
    return projects


def get_project_by_pid(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    return project


def get_projects_assigned(mongo, user):
    assignments = mongo.db.projects.find({'assignee': user})
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

    return assignee_stat[user_idx]
    current_page = assignee_stat[user_idx]['current_page']
    page_size = assignee_stat[user_idx]['page_size']
    kapr_limit = assignee_stat[user_idx]['kapr_limit']
    current_kapr = assignee_stat[user_idx]['current_kapr']

    ret = {
        'current_page': int(current_page),
        'page_size': int(page_size),
        'kapr_limit': float(kapr_limit),
        'current_kapr': float(current_kapr)
    }

    return ret


def get_assignee_result_path(mongo, pid, assignee):
    assignment = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = assignment['assignee_stat']

    for item in assignee_stat:
        if item['assignee'] == assignee:
            return item['result_path']


def increase_assignment_page(mongo, username, pid):
    assignment = mongo.db.projects.find_one({'pid': pid})
    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": username}, {"$inc": {"assignee_stat.$.current_page": 1}})


def increase_conflict_page_pairidx(mongo, username, pid):
    project = mongo.db.conflicts.find_one({'pid': pid})
    current_page = int(project['current_page'])
    mongo.db.conflicts.update({"pid": pid}, {"$inc": {"current_page": 1}})

    block_id = project['pair_num']
    inc = len(block_id[current_page])
    mongo.db.conflicts.update({"pid": pid}, {"$inc": {"pair_idx": inc}})

def increase_pair_idx(mongo, pid, username):
    assignment = mongo.db.projects.find_one({'pid': pid})

    pair_idx = 0
    assignee_stat = assignment['assignee_stat']
    for item in assignee_stat:
        if item['assignee'] == username:
            assignee = item
            break

    pair_idx = assignee['pair_idx']
    assigned_id = assignee['assigned_id']

    pos, i = 0, 0
    while pair_idx != pos and i < len(assigned_id):
        pos += len(assigned_id[i])
        i += 1
    inc = len(assigned_id[i])

    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": username}, {"$inc": {"assignee_stat.$.pair_idx": inc}})


def update_kapr(mongo, username, pid, kapr):
    assignment = mongo.db.projects.find_one({'pid': pid})
    mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": username}, {"$set": {"assignee_stat.$.current_kapr": kapr}})

def update_kapr_conflicts(mongo, username, pid, kapr):
    mongo.db.conflicts.update({'pid': pid}, {'$set': {'current_kapr': kapr}})

def get_data_mode(assignment_id, ids, r, default_mode='M'):
    """
    if is None, then insert 'M' into the redis
    """
    mode_dict = {'M': 'masked', 'P': 'partial', 'F': 'full', 'B': 'base'}
    data_mode_list = []

    for (id1, id2) in ids:
        cur_list = []
        for attribute_id1 in id1:
            key = assignment_id + '-' + attribute_id1
            mode = r.get(key)
            if mode != None:
                if mode in ['masked', 'partial', 'full', 'base']:
                    cur_list.append(mode)
                else:
                    cur_list.append(mode_dict[mode])
            else:
                r.set(key, default_mode)
                cur_list.append(mode_dict[default_mode])
        data_mode_list.append(cur_list)

    return data_mode_list


def _union_data_mode(list1, list2):
    ret = 11*['masked']
    for i in range(11):
        if list1[i] == 'full' or list2[i] == 'full':
            ret[i] = 'full'
        elif list1[i] == 'partial' or list2[i] == 'partial':
            ret[i] = 'partial'
    return ret


def get_conflict_data_mode(pid, ids, mongo, r, manager_assignment_id, isfull=False):
    """
    the data mode for resolve conflicts is the Union of each assignee's data mode
    """
    if isfull:
        data_mode_list = len(ids)*[11*['base']]
        return data_mode_list

    data_mode_list = len(ids)*[11*['masked']]

    project = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        username = assignee['assignee']
        assignment_id = pid + '-' + username
        cur_data_mode_list = get_data_mode(assignment_id, ids, r)
        
        for i in range(len(ids)):
            data_mode_list[i] = _union_data_mode(data_mode_list[i], cur_data_mode_list[i])

            # insert data mode to redis as manager role
            id1, id2 = ids[i]
            j = 0
            for attribute_id1 in id1:
                key = manager_assignment_id + '-' + attribute_id1
                r.set(key, data_mode_list[i][j])
                j += 1

    return data_mode_list


def get_pair_datafile(mongo, user, pid):
    assignment = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = assignment['assignee_stat']
    for item in assignee_stat:
        if item['assignee'] == user.username:
            return item['pf_path']

def get_pair_datafile_by_owner(mongo, owner, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    return project['pf_path']

def get_project_pair_datafile(mongo, user, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    if project['owner'] == user or True:
        return project['pf_path']
    else:
        print('ERROR-storage_model.get_project_pair_datafile')
        return project['pf_path']


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


def save_answers(mongo, pid, username, data):
    """
    save one page answers to file
    """
    data_to_write = list()

    for d in data:
        if d['type'] == 'final_answer':
            answer = d['value']
            pair_num = int(answer.split('a')[0][1:])
            choice = int(answer.split('a')[1])
            decision = 1 if choice > 3 else 0
            line = ','.join([str(pair_num), str(decision), str(choice)])
            data_to_write.append(line)

    filename = get_assignee_result_path(mongo=mongo, pid=pid, assignee=username)

    with open(filename, 'a') as f:
        for item in data_to_write:
            f.write(item + '\n')

    return True


def update_resolve_conflicts(mongo, pid):
    """
    update the result file
    if pair_id not in the conflicts: copy it to the final result
    else: use the resolve conflicts result as the final result
    """
    conflict_project = mongo.db.conflicts.find_one({'pid': pid})
    conflict_result = conflict_project['result_path']

    final_answer = dict()
    with open(conflict_result, 'r') as fin:
        for line in fin:
            answer = line.rstrip().split(',')
            pair_num = int(answer[0])
            final_answer[pair_num] = line.rstrip()

    project = mongo.db.projects.find_one({'pid': pid})
    result_file = project['result_path']

    results = dict()
    with open(result_file, 'r') as fin:
        for line in fin:
            if line.strip() == '':
                continue
            pair_id, decision, choice = line.strip().split(',')
            if int(pair_id) in final_answer:
                results[int(pair_id)] = final_answer[int(pair_id)]
            else:
                results[int(pair_id)] = line.strip()

    with open(result_file, 'w+') as fout:
        for pair_id in sorted(results):
            fout.write(results[pair_id]+'\n')

    return True


def save_resolve_conflicts(mongo, pid, username, data):
    """
    save the resolve conflicts result file
    """
    data_to_write = list()

    for d in data:
        if d['type'] == 'final_answer':
            answer = d['value']
            pair_num = int(answer.split('a')[0][1:])
            choice = int(answer.split('a')[1])
            decision = 1 if choice > 3 else 0
            line = ','.join([str(pair_num), str(decision), str(choice)])
            data_to_write.append(line)

    project = mongo.db.conflicts.find_one({'pid': pid})
    filename = project['result_path']

    print(filename)

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

def is_conflict_project_completed(mongo, pid):
    project = mongo.db.conflicts.find_one({'pid': pid})

    if int(project['current_page']) < int(project['page_size']):
        return False
    return True
    

def update_project_setting(mongo, user, data):
    pid = data['pid']
    #project_name = data['project_name']
    project_des = data['project_des']
    #assignee = data['assignee']
    #kapr_limit = data['kapr_limit']

    #mongo.db.projects.update({"pid": pid}, {"$set": {"project_name": project_name, "project_des": project_des}})
    mongo.db.projects.update({"pid": pid}, {"$set": {"project_des": project_des}})

    #mongo.db.projects.update( {"pid": pid, "assignee_stat.assignee": assignee}, {"$set": {"assignee_stat.$.kapr_limit": float(kapr_limit)}})

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


def get_current_block(mongo, pid, assignee):
    """
    get pair id for current block (one block per page)
    """
    assignment = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = assignment['assignee_stat']

    for item in assignee_stat:
        if item['assignee'] == assignee:
            cur_assignee = item
            break

    pair_idx = cur_assignee['pair_idx']
    assigned_id = cur_assignee['assigned_id']

    pos = 0
    i = 0
    while pair_idx != pos and i < len(assigned_id):
        pos += len(assigned_id[i])
        i += 1

    ret = assigned_id[i]

    return ret, pair_idx

def get_record_id_by_pair_id(mongo, pid, indices):
    project = mongo.db.projects.find_one({'pid': pid})
    pairfile_path = project['pairfile_path']

    id_dict = dict()
    with open(pairfile_path, 'r') as fin:
        lines = fin.readlines()
        for i in range(1, len(lines), 2):
            line1 = lines[i]
            line2 = lines[i+1]
            data1 = line1.split(',')
            data2 = line2.split(',')
            if project['created_by'] == 'pairfile':
                id1 = data1[2]+'-'+data1[3]
                id2 = data2[2]+'-'+data2[3]
                pid = data1[0]
            else:
                id1 = data1[8]
                id2 = data2[8]
                pid = data1[0]
            id_dict[int(pid)] = (id1, id2)

    ret = list()
    for pair_id in indices:
        ret.append(id_dict[int(pair_id)])
    return ret

def combine_result(mongo, pid):
    """
    combine assignee result file into final result file.
    if the answer are the same, just keep one.
    """
    project = mongo.db.projects.find_one({'pid': pid})

    result_file = project['result_path']
    pairfile_path = project['pairfile_path']

    results = list()
    answers = dict()
    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        cur_result = assignee['result_path']
        with open(cur_result, 'r') as fin:
            for line in fin:
                if line:
                    pair_id, decision, choice = line.rstrip().split(',')
                    pair_id = int(pair_id)
                    decision = int(decision)
                    if pair_id not in answers:
                        answers[pair_id] = decision
                        results.append(line)
                    else:
                        if answers[pair_id] == decision:
                            continue
                        else:
                            results.append(line)

        # reset (cannot reset yet. resolve conflict need assignee's result)
        #with open(cur_result, 'w+') as fout:
        #    fout.write('')

    with open(result_file, 'a') as fout:
        for item in results:
            fout.write(item)

    return True

def delete_resolve_conflict(mongo, pid):
    project = mongo.db.conflicts.find_one({'pid': pid})
    result_file = project['result_path']
    delete_file(result_file)
    ret = mongo.db.conflicts.delete_one({'pid': pid})
    return ret


def update_result(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})

    if project['created_by'] == 'pairfile':
        return True

    result_file = project['result_path']
    pairfile_path = project['pairfile_path']
    intfile_path = project['intfile_path']

    update_result_to_intfile(result_file, pairfile_path, intfile_path)

    # reset result file
    fout = open(result_file, 'w+')
    fout.close()

    return True


def generate_final_result(pairfile_path, result_path, final_result_path):
    result = dict()
    with open(result_path, 'r') as fin:
        for line in fin:
            data = line.strip().split(',')
            result[int(data[0])] = [int(data[1]), int(data[2])]

    table_head = 'PairID,GroupID,DB,ID,voter_reg_num,first_name,last_name,dob,sex,race,info1,info2,info3,info4,info5,decision,choice\n'
    f1 = open(pairfile_path, 'r')
    f2 = open(final_result_path, 'w')

    cnt = 0
    for line in f1:
        if cnt == 0:
            f2.write(table_head)
        else:
            data = line.strip().split(',')
            pair_id = int(data[0])
            res = result[pair_id]
            newline = line.rstrip() + ',' + str(res[0]) + ',' + str(res[1]) + '\n'
            f2.write(newline)
        cnt += 1

    f1.close()
    f2.close()


def get_result_path(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    if project['created_by'] == 'pairfile':
        generate_final_result(project['pairfile_path'], project['result_path'], project['final_result_path'])
        return project['final_result_path']
    else:
        return project['intfile_path']


def detect_result_conflicts(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})

    result_file = project['result_path']

    pair_id = dict()
    conflicts = set()
    with open(result_file, 'r') as fin:
        for line in fin:
            if line.strip() == '':
                continue
            data = line.split(',')
            cur_id = int(data[0])
            if cur_id in pair_id:
                conflicts.add(cur_id)
            else:
                pair_id[cur_id] = 1

    return list(conflicts)

def save_conflict_project(mongo, data):
    mongo.db.conflicts.insert(data)
    return True

def get_conflict_project(mongo, username, pid):
    project = mongo.db.conflicts.find_one({'pid': pid})
    return project


def get_users_choices(mongo, pid, indices):
    """
    Retures:
        {
            pair_num: [[username, decision, choice], [username, decision, choice]],
            pair_num: [[username, decision, choice], [username, decision, choice]],
        }
    """
    choices = defaultdict(list)
    choice_map = {1:'H', 2:'M', 3:'L', 4:'L', 5:'M', 6:'H'}

    project = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        result_path = assignee['result_path']
        with open(result_path, 'r') as fin:
            data = fin.readlines()
            answers = [line.rstrip().split(',') for line in data if len(line.rstrip()) > 0]
            for answer in answers:
                if int(answer[0]) in indices:
                    choices[int(answer[0])].append([assignee['assignee'], int(answer[1]), choice_map[int(answer[2])]])

    choice_cnt = dict()
    for idx in indices:
        choice_cnt[idx] = list([0, 0])
    for k, v in choices.items():
        for item in v:
            decision = item[1]
            choice_cnt[k][decision] += 1

    return choices, choice_cnt

def has_full_assignee(mongo, pid):
    project = mongo.db.projects.find_one({'pid': pid})
    assignee_stat = project['assignee_stat']
    for assignee in assignee_stat:
        if assignee['isfull'] == 'true':
            return True
    return False

def new_blocking(mongo, data):
    project = mongo.db.projects.find_one({'pid': data['pid']})
    pid=data['pid']
    project_name = project['project_name']
    owner = project['owner']
    assignee = project['assignee'][0]
    file1_path = project['file1_path']
    file2_path = project['file2_path']
    intfile_path = project['intfile_path']
    pairfile_path = project['pairfile_path']

    total_pairs, block_id = blocking.new_blocking(blocking=data['blocking'], intfile=intfile_path, pair_file=pairfile_path)

    assigner = Assign_generator(pairfile_path)
    assignee_items = data['assignee_area'].rstrip(';').split(';')
    assignee_list = list()
    assignee_stat = list()
    for assignee_item in assignee_items:
        cur_assignee, cur_kapr, cur_percentage = assignee_item.split(',')
        assignee_list.append(cur_assignee)

        percentage = float(cur_percentage)/100.0
        tmp_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+cur_assignee+'_'+project_name+'_pairfile.csv')
        #assigned_id = random_assign(pair_file=pairfile_path, tmp_file=tmp_file, pair_num=int(total_pairs*percentage), block_id=block_id)
        assigned_id = assigner.random_assign(tmp_file=tmp_file, pair_num=int(total_pairs*percentage), block_id=block_id)
        pf_file = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_pf.csv')
        pf_result = generate_pair_file(tmp_file, file1_path, file2_path, pf_file)
        delete_file(tmp_file)

        total_blocks = get_block_num(block_id=block_id, pf_file=pf_file)

        # create result file
        cur_result = os.path.join(config.DATA_DIR, 'internal', owner+'_'+project_name+'_'+cur_assignee+'_result.csv')
        f = open(cur_result, 'w+')
        f.close()

        assignee_stat.append({
            'assignee': cur_assignee, 
            'pf_path': pf_file,
            'result_path': cur_result,
            'assigned_id': assigned_id,
            'current_page': 0, 
            'page_size': total_blocks, 
            'kapr_limit': cur_kapr, 
            'current_kapr': 0,
            'pair_idx': 0,
            'total_pairs': pf_result['size'],
        })

    mongo.db.projects.update( {"pid": pid}, {"$set": {"assignee": assignee_list}})
    mongo.db.projects.update( {"pid": pid}, {"$set": {"assignee_stat": assignee_stat}})

    return pid


def mlog(mongo, data):
    mongo.db.log.insert(data)



