import os
import json

def kv_pairs2dict(kv_pairs):
    ret = dict()
    for kv in kv_pairs:
        k, v = kv.split(':')
        ret[k] = v
    return ret

def append_log(filename):
    data = list()
    with open(filename, 'r') as fin:
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
                        data.append('%s,%s,%s,%s,%s,%s,%s\n'%(item['timestamp'],item['username'],item['pid'],kv_dict['id'],kv_dict['type'],kv_dict['value'],row))
                    elif kv_dict['type'] == 'final_answer':
                        pair_id = kv_dict['value'].split('a')[0][1:]
                        choice = kv_dict['value'].split('a')[1]
                        data.append('%s,%s,%s,%s,%s,%s,%s\n'%(item['timestamp'],item['username'],item['pid'],pair_id,kv_dict['type'],choice,row))
            elif item['url'] == '/get_cell' or item['url'] == '/get_big_cell':
                content = item['log']
                log_content = json.loads(content)
                if 'id' not in log_content:
                    continue
                pair_id = log_content['id']
                data.append('%s,%s,%s,%s,%s,%s,%s\n'%(item['timestamp'],item['username'],item['pid'],pair_id,'click',log_content['KAPR'],content))
    #print(len(data))
    return data


files = ['round1/mindfirl/log_round1_gurudev.json',
'round1/mindfirl/log_round1_sulki.json',
'round1/mindfirl/log_round1_theodoros.json',
'round1/mindfirl/log_round1_alejandro.json',
'round1/control/log_round1_reuben.json',
'round1/control/log_round1_heath.json',
'round1/control/log_round1_mahin.json',
'round1/control/log_round1_qinbo.json',
'round2/mindfirl/log_round_2_1_alejandro.json',
'round2/mindfirl/log_round_2_2_alejandro.json',
'round2/mindfirl/log_round_2_2_theodoros.json',
'round2/mindfirl/log_round_2_3_gurudev.json',
'round2/mindfirl/log_round_2_3_sulki.json',
'round2/mindfirl/log_round_2_4_sulki.json',
'round2/control/log_control_round_2_1.json',
'round2/control/log_control_round_2_2.json',
'round2/control/log_control_round_2_3.json',
'round2/control/log_control_round_2_4.json',
'round3/mindfirl/log_mindfirl_conflicts.json',
]


with open('log_full.csv', 'w') as fout:
    for f in files:
        fout.write('timestamp,username,project_name,pid,type,value,info\n')
        
        data = append_log(f)
        print(len(data))

        for d in data:
            fout.write(d)

