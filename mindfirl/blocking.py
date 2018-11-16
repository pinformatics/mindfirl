from collections import defaultdict


def eq(r1, r2, attrs):
    for idx in attrs:
        if r1[idx] != r2[idx]:
            return False
    return True


def hamming_distance(r1, r2):
    distance = 0
    for i in range(1, len(r1)):
        if r1[i] != r2[i]:
            distance += 1
    return distance


def generate_pairs(block, start_id):
    """
    find a centroid: have a minimum average hamming distance to other records.
    build pairs between centroid and others.
    """
    m_distance = 6*len(block)
    m_idx = 0

    for i in range(len(block)):
        current = block[i]
        distance = 0
        for j in range(len(block)):
            if i == j:
                continue
            distance += hamming_distance(block[i], block[j])
        if distance < m_distance:
            m_distance = distance
            m_idx = i

    pairs = list()
    pid = start_id
    for i in range(len(block)):
        if i == m_idx:
            continue
        pairs.append([pid, block[m_idx][1], block[m_idx][2], block[m_idx][3], block[m_idx][4], block[m_idx][5], block[m_idx][6], 1, block[m_idx][0]])
        pairs.append([pid, block[i][1], block[i][2], block[i][3], block[i][4], block[i][5], block[i][6], 1, block[i][0]])
        pid += 1

    return pairs


def blocking_and_generate_pairs(blocking, intfile, pair_file):
    db = list()
    with open(intfile, 'r') as fin:
        pos = 0
        for line in fin:
            if len(line) == 0 or line == "\n":
                continue

            data = line.rstrip('\n').split(',')
            if pos == int(data[7]):
                db.append(data)

            pos += 1

    attribute = { 'id': 1, 'fn': 2, 'ln': 3, 'bd': 4, 'gd': 5, 'rc': 6 }
    sorting_keys = list()
    for block_attr in blocking:
        if block_attr in attribute:
            sorting_keys.append(attribute[block_attr])

    if not sorting_keys:
        db_sorted = sorted(db, key=lambda x: (x[0]))
    elif len(sorting_keys) == 1:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]]))
    elif len(sorting_keys) == 2:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]], x[sorting_keys[1]]))
    elif len(sorting_keys) == 3:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]], x[sorting_keys[1]], x[sorting_keys[2]]))
    elif len(sorting_keys) == 4:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]], x[sorting_keys[1]], x[sorting_keys[2]], x[sorting_keys[3]]))
    elif len(sorting_keys) == 5:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]], x[sorting_keys[1]], x[sorting_keys[2]], x[sorting_keys[3]], x[sorting_keys[4]]))
    elif len(sorting_keys) == 6:
        db_sorted = sorted(db, key=lambda x: (x[sorting_keys[0]], x[sorting_keys[1]], x[sorting_keys[2]], x[sorting_keys[3]], x[sorting_keys[4]], x[sorting_keys[5]]))

    print('finished sorting db.')

    data_pair = list()
    i = 0
    while i < len(db_sorted):
        block = [db_sorted[i]]
        while i+1 < len(db_sorted) and eq(block[0], db_sorted[i+1], sorting_keys):
            block.append(db_sorted[i+1])
            i += 1
        if len(block) >= 2:
            pairs = generate_pairs(block, start_id=int(len(data_pair)/2+1))
            data_pair += pairs

        i += 1

    if len(data_pair) == 0:
        return False

    print('finished generate pairs.')

    with open(pair_file, 'w+') as fout:
        fout.write('ID,voter_reg_num,first_name,last_name,dob,sex,race,type,file_id\n')
        for dp in data_pair:
            fout.write(','.join([str(x) for x in dp])+'\n')

    print('finished writing data pairs.')

    return True


def create_intfile(file1, file2, intfile):
    db = list()
    paird_data = list()

    ids = defaultdict(int)

    # mindfirl internal id
    iid = 0

    with open(file1, 'r') as fin:
        i = 0
        for line in fin:
            if len(line) == 0 or line == "\n":
                continue
            if i > 0:
                data = line.rstrip('\n').split(',')
                for j in range(len(data)):
                    data[j] = data[j].strip(' ')

                data_id = 'A' + data[0]
                data[0] = data_id
                if data_id not in ids:
                    ids[data_id] += 1
                    data.append(iid)
                    iid += 1
                    db.append(data)
            i += 1

    with open(file2, 'r') as fin:
        i = 0
        for line in fin:
            if len(line) == 0 or line == "\n":
                continue
            if i > 0:
                data = line.rstrip('\n').split(',')
                for j in range(len(data)):
                    data[j] = data[j].strip(' ')

                data_id = 'B' + data[0]
                data[0] = data_id
                if data_id not in ids:
                    ids[data_id] += 1
                    data.append(iid)
                    iid += 1
                    db.append(data)
            i += 1

    with open(intfile, 'w+') as fout:
        for row in db:
            fout.write(','.join([str(x) for x in row])+'\n')
    print("finished reading file1 and file2. length of data is" + str(len(db)))


def generate_pair_by_blocking(blocking, file1, file2, intfile, pair_file):
    """
    input: 
        blocking: attribute to block
        file1: data file 1
        file2: data file 2
        intfile: intermediate file path
        pair_file: output path
    """

    # create intfile
    create_intfile(file1, file2, intfile)

    return blocking_and_generate_pairs(blocking, intfile, pair_file)


def new_blocking(blocking, intfile, pair_file):
    return blocking_and_generate_pairs(blocking, intfile, pair_file)


def get_id_by_pair_id(pair_id, pairs):
    data = pairs[pair_id]
    return data[0][8], data[1][8]



def find_pos_by_iid(int_data, iid):
    for i in range(len(int_data)):
        if int_data[i][0] == iid:
            return i
    return None


def disjoint_find_root(int_data, pos):
    if int(int_data[pos][7]) == pos:
        return pos
    return disjoint_find_root(int_data, int(int_data[pos][7]))


def disjoint_merge(int_data, iid1, iid2):
    """
    int_data: 
    iid,id,fn,ln,dob,sex,race,gid,pos
    A1,1000000657,LYNN,WILDING,07/04/1946,M,W,0
    A2,1000000623,LYNN,WILDING,07/05/1946,M,W,1
    """
    pos1 = find_pos_by_iid(int_data, iid1)
    pos2 = find_pos_by_iid(int_data, iid2)
    root1 = disjoint_find_root(int_data, pos1)
    root2 = disjoint_find_root(int_data, pos2)
    int_data[root2][7] = root1



def update_result_to_intfile(result_file, pair_file, intfile):
    # read current round result
    current_result = list()
    with open(result_file, 'r') as fin:
        for line in fin:
            data = line.strip('\n').split(',')
            current_result.append(data)

    # read pair file
    pairs = defaultdict(list)
    with open(pair_file, 'r') as fin:
        i = 0
        for line in fin:
            if i > 0:
                data = line.rstrip('\n').split(',')
                pair_id = data[0]
                pairs[pair_id].append(data)
            else:
                i += 1

    # read int file
    int_data = list()
    with open(intfile, 'r') as fin:
        for line in fin:
            data = line.rstrip('\n').split(',')
            int_data.append(data)

    for result in current_result:
        if int(result[1]) == 1:
            pair_id = result[0]
            # iid1 is always the centroid
            iid1, iid2 = get_id_by_pair_id(pair_id=pair_id, pairs=pairs)

            disjoint_merge(int_data, iid1, iid2)

    # write to file
    with open(intfile, 'w') as fout:
        for data in int_data:
            fout.write(','.join([str(x) for x in data])+'\n')







