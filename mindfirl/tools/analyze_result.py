import os
import json

def count_choice(filename):
    data = list()
    with open(filename, 'r') as fin:
        for line in fin:
            data.append(line.strip().split(','))
    
    D_cnt = 0
    S_cnt = 0
    DH = 0
    DM = 0
    DL = 0
    SL = 0
    SM = 0
    SH = 0
    for item in data:
        if item[1] == '0':
            D_cnt += 1
        else:
            S_cnt += 1
        if item[2] == '1':
            DH += 1
        elif item[2] == '2':
            DM += 1
        elif item[2] == '3':
            DL += 1
        elif item[2] == '4':
            SL += 1
        elif item[2] == '5':
            SM += 1
        else:
            SH += 1
    print('D, S, DH, DM, DL, SL, SM, SH')
    print(D_cnt, S_cnt, DH, DM, DL, SL, SM, SH)

def get_accuracy(result_file, answer_file):
    answers = dict()
    with open(answer_file, 'r') as fin:
        i = 0
        for line in fin:
            if i == 0:
                i += 1
                continue
            pid, ans = line.strip().split(',')
            pid = int(pid)
            answers[pid] = ans

    correct = 0
    wrong = 0
    with open(result_file, 'r') as fin:
        for line in fin:
            pid, decision, choice = line.strip().split(',')
            pid = int(pid)
            decision = int(decision)
            ans = answers[pid]
            if (decision == 0 and ans == 'unmatch') or (decision == 1 and ans == 'match'):
                correct += 1
            else:
                wrong += 1
    accuracy = (1.0*correct/(correct+wrong))
    print(accuracy)

def get_hover_count(log_file):
    count = 0
    hover_count = 0
    with open(log_file, 'r') as fin:
        for line in fin:
            item = json.loads(line)
            if item['url'] == '/save_data':
                count += 1
                content = item['log']
                rows = content.strip().split(';')
                for row in rows:
                    if not row:
                        continue
                    kv_pairs = row.split(',')
                    for kv in kv_pairs:
                        k, v = kv.split(':')
                        if k == 'type' and v == 'hover':
                            hover_count += 1
    print(hover_count)

def kv_pairs2dict(kv_pairs):
    ret = dict()
    for kv in kv_pairs:
        k, v = kv.split(':')
        ret[k] = v
    return ret

def get_hover_and_click_count(log_file):
    hover_ids = set()
    click_ids = set()
    with open(log_file, 'r') as fin:
        for line in fin:
            item = json.loads(line)
            if item['url'] == '/save_data':
                content = item['log']
                rows = content.strip().split(';')
                for row in rows:
                    if not row:
                        continue
                    kv_pairs = row.split(',')
                    kv_dict = kv_pairs2dict(kv_pairs)
                    if kv_dict['type'] == 'hover':
                        hover_ids.add(kv_dict['id'])
            elif item['url'] == '/get_cell' or item['url'] == '/get_big_cell':
                content = item['log']
                log_content = json.loads(content)
                pid = log_content['id']
                click_ids.add(pid)

    hover_and_click = hover_ids.intersection(click_ids)

    print(len(click_ids))
    print(len(hover_ids))
    print(len(hover_and_click))

def main():
    #filename = 'round1/control/mahin_control_round_1_reuben_result.csv'
    #count_choice('round3/mindfirl/gurudev_mindfirl_conflicts_result.csv')
    #get_accuracy('round3/control/mahin_control_conflicts_result.csv', 'answer_key.csv')
    #get_hover_count('round1/mindfirl/log_round1_theodoros.json')
    get_hover_and_click_count('log_mindfirl_conflicts.json')

if __name__ == '__main__':
    main()

