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


def generate_pair_by_blocking(blocking, file1, file2, pair_file):
    db = list()
    paird_data = list()

    ids = defaultdict(int)

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
                    db.append(data)
            i += 1

    print("finished reading file1 and file2. length of data is" + str(len(db)))

    attribute = { 'id': 1, 'fn': 2, 'ln': 3, 'bd': 4, 'gd': 5, 'rc': 6 }
    sorting_keys = list()
    for block_attr in blocking:
        if block_attr in attribute:
            sorting_keys.append(attribute[block_attr])

    print(sorting_keys)

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

    print('finished generate pairs.')

    with open(pair_file, 'w+') as fout:
        fout.write('ID,voter_reg_num,first_name,last_name,dob,sex,race,type,file_id\n')
        for dp in data_pair:
            fout.write(','.join([str(x) for x in dp])+'\n')

    print('finished writing data pairs.')
