import os

def select_pairs(pair_id_file, pair_file, out_file):
    pid = set()
    with open(pair_id_file, 'r') as fin:
        for line in fin:
            cur_pid = int(line.strip())
            pid.add(cur_pid)


    conflicts = list()
    head = ''
    with open(pair_file, 'r') as fin:
        i = 0
        for line in fin:
            if i > 0:
                cur_pid = int(line.strip().split(',')[0])
                if cur_pid in pid:
                    conflicts.append(line)
            else:
                head = line
            i += 1

    with open(out_file, 'w+') as fout:
        fout.write(head)
        for line in conflicts:
            fout.write(line)


select_pairs('data/ids.csv', 'data/pairfile_new_sample.csv', 'data/conflicts_sample.csv')
