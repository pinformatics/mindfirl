 #! /usr/bin/python
# encoding=utf-8

import logging
import copy
import data_model as dm


def format_user_data(data):
    formatted_data = ''
    pkeys = ['uid', 'type', 'value', 'timestamp']
    for k in pkeys:
        if formatted_data:
            formatted_data += (',' + k + ':' + str(data[k]))
        else:
            formatted_data += (k + ':' + str(data[k]))

    for k in sorted(data):
        if k not in pkeys:
            formatted_data += (',' + k + ':' + str(data[k]))

    formatted_data += ';'
    return formatted_data


def parse_user_data(user_data):
    """
    input: string, user data from front end.
    output: a list of dict
    """
    if not user_data:
        return []
    user_data_list = user_data.split(';')
    ret = list()
    for i in range(len(user_data_list)):
        data = user_data_list[i].strip().rstrip('\n').rstrip(';')
        if data:
            data_dict = dict()
            kv_pairs = data.split(',')
            for kv in kv_pairs:
                if len(kv.split(':')) == 2:
                    k = kv.split(':')[0].strip()
                    v = kv.split(':')[1].strip()
                    data_dict[k] = v
            if len(data_dict) > 0:
                ret.append(data_dict)
    return ret


def grade_final_answer(data, data_pair_list):
    size = data_pair_list.size()
    correct = 0
    for d in data:
        # print 'url' not in d or'/main_section/' in d['url']
        if 'type' not in d or d['type'] != 'final_answer':
            continue
        if 'url' not in d:
            continue
        if not d['url'] == '/record_linkage' and not '/main_section' in d['url']:
            continue

        answer_id = d['value']
        answer_id = answer_id.lstrip('p')
        pair_num = int(answer_id.split('a')[0])
        answer = int(answer_id.split('a')[1])

        dp = data_pair_list.get_data_pair(pair_num)
        if dp != None and dp.grade(answer):
            correct += 1

    return [correct, size]