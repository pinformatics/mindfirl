import csv
from collections import defaultdict

def substring_at_ends(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    finalStr1 = ""
    finalStr2 = ""
    if s1.startswith(s2):
        if (len1-len2)/float(len(s1)) > 0.5:
            finalStr1 = s1
            finalStr2 = s2
        else:
            for i in range(len(s2)):
                finalStr2 = finalStr2 + "*"
                finalStr1 = finalStr1 + "*"
            for i in range(len(s2),len(s1)):
                finalStr1 = finalStr1 + s1[i]
                finalStr2 = finalStr2 + "_"
    elif s1.endswith(s2):
        if (len1-len2)/float(len(s1)) > 0.5:
            finalStr1 = s1
            finalStr2 = s2
        else:
            for i in range(len(s1)-1,len(s1)-len(s2)-1,-1):
                finalStr2 = "*" + finalStr2
                finalStr1 = "*" + finalStr1
            for i in range(len(s1)-len(s2)-1,-1,-1):
                finalStr1 = s1[i] + finalStr1
                finalStr2 = "_" + finalStr2

    return finalStr1,finalStr2



def get_edit_distance(s1, s2, title=''):

    finalStr1 = ""
    finalStr2 = ""

    if len(s1)==0:
        return "", s2
    if len(s2)==0:
        return s1, ""

    len1 = len(s1)
    len2 = len(s2)

    if len1 > len2:
        finalStr1,finalStr2 = substring_at_ends(s1,s2)
    elif len2>len1:
        finalStr2, finalStr1 = substring_at_ends(s2, s1)

    if len(finalStr1)==0 and len(finalStr2)==0:
        dp = {}
        direction = {}
        for i in range(len1 + 1):
            dp[i] = {}
            direction[i] = {}
            for j in range(len2 + 1):
                dp[i][j] = []
                direction[i][j] = []

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                    direction[i][j] = 'd'
                elif j == 0:
                    dp[i][j] = i
                    direction[i][j] = 'i'

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                    direction[i][j] = 'd'
                elif j == 0:
                    dp[i][j] = i
                    direction[i][j] = 'i'
                elif s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                    direction[i][j] = 'n'
                else:

                    insertVal = dp[i - 1][j] + 1
                    deleteVal = dp[i][j - 1] + 1
                    subsVal = dp[i - 1][j - 1] + (0 if s1[i - 1] == s2[j - 1] else 1)
                    transVal = 1000000000
                    if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1] and s1[i - 1] != s1[i - 2]:
                        transVal = dp[i - 2][j - 2]
                    minAll = min([insertVal, deleteVal, subsVal, transVal])
                    if title=='ID':
                        dp[i][j] = minAll + 1
                    else:
                        dp[i][j] = minAll

                    if minAll == transVal:
                        direction[i][j] = 't'
                    elif minAll == insertVal:
                        direction[i][j] = 'i'
                    elif minAll == deleteVal:
                        direction[i][j] = 'd'
                    else:
                        if s1[i - 1] == s2[j - 1]:
                            direction[i][j] = 'n'
                        else:
                            direction[i][j] = 's'

                            # dp[i][j] = minAll + 1

        stI = len1
        stJ = len2
        while stI > 0 or stJ > 0:
            if direction[stI][stJ] == 'i':
                finalStr1 = s1[stI - 1] + finalStr1
                finalStr2 = "_" + finalStr2
                stI = stI - 1

            elif direction[stI][stJ] == 'd':
                finalStr1 = "_" + finalStr1
                finalStr2 = s2[stJ - 1] + finalStr2
                stJ = stJ - 1

            elif direction[stI][stJ] == 's':
                finalStr1 = s1[stI - 1] + finalStr1
                finalStr2 = s2[stJ - 1] + finalStr2
                stI = stI - 1
                stJ = stJ - 1

            elif direction[stI][stJ] == 'n':
                finalStr1 = "*" + finalStr1
                finalStr2 = "*" + finalStr2
                stI = stI - 1
                stJ = stJ - 1

            else:
                finalStr1 = s1[stI - 2] + s1[stI - 1] + finalStr1
                finalStr2 = s2[stJ - 2] + s2[stJ - 1] + finalStr2
                stI = stI - 2
                stJ = stJ - 2

    return finalStr1, finalStr2

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]

def hamming_with_transpose(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(500,d[(i - 1, j - 1)] + cost,) # substitution

            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]

def check_starring(s1, s2):
    len_1 = len(s1)
    len_2 = len(s2)
    if(len_1 >= len_2):
        if s1[:len_2] == s2:
            return True
        elif s1[len(s1)-len(s2):] == s2:
            return True
        b_len = len_1
    else:
        if s2[:len_1] == s1:
            return True
        elif s2[len(s2)-len(s1):] == s1:
            return True
        b_len = len_2
    edit_distance = damerau_levenshtein_distance(s1, s2)

    if float(edit_distance)/b_len > 0.5:
        return False
    return True

def format_date(x):
    return(x[:2] + '/' + x[2:4] + '/' + x[4:])

def get_star_date(date_1, date_2):
    #print(date_1, date_2)
    if (len(date_1) < 10) & (len(date_2) < 10):
        return "", ""
    if len(date_1) < 10:
        return "", format_date(date_2[:2] + date_2[3:5] + date_2[6:])
    if len(date_2) < 10:
        return format_date(date_1[:2] + date_1[3:5] + date_1[6:]), ""

    day_1 = date_1[:2]
    day_2 = date_2[:2]

    month_1 = date_1[3:5]
    month_2 = date_2[3:5]

    year_1 = date_1[6:]
    year_2 = date_2[6:]

    year_1_star= ""
    year_2_star= ""
    if not day_1 == month_1 and not day_2 == month_2:
        if month_1 == day_2 and month_2 == day_1:
            for i in range(4):
                if year_1[i] == year_2[i]:
                    year_1_star = year_1_star + "*"
                    year_2_star = year_2_star + "*"
                else:
                    year_1_star = year_1_star + year_1[i]
                    year_2_star = year_2_star + year_2[i]
            return format_date(date_1[:2] + date_1[3:5] + year_1_star), format_date(date_2[:2] + date_2[3:5] + year_2_star)

    if not day_1 == day_2:
        if not month_1 == month_2:
            if not year_1 == year_2:
                return format_date(date_1[:2] + date_1[3:5] + date_1[6:]), format_date(date_2[:2] + date_2[3:5] + date_2[6:])

    final_1 = ""
    final_2 = ""
    ind = [0,1,3,4,6,7,8,9]

    for i in ind:
        if date_1[i] == date_2[i]:
            final_1 = final_1 + "*"
            final_2 = final_2 + "*"
        else:
            final_1 = final_1 + date_1[i]
            final_2 = final_2 + date_2[i]
    return format_date(final_1),format_date(final_2)

def trailing_space_symbol(str):
    str = list(str)
    for i in range((len(str) - 1), -1, -1):
        if str[i] == "_":
            str[i] = "?"
        else:
            break;
    str = "".join(str)
    return str

def get_star_vot_reg(n1, n2):
    n1 = str(n1)
    n2 = str(n2)

    #if (len(n1) < 10 and len(n2) < 10): return "",""
    #if len(n1) < 10: return "", n2
    #if len(n2) < 10: return n1, ""

    len_1 = len(n1)
    len_2 = len(n2)

    if not len_1 == len_2:
        return n1, n2

    hamm_trans = damerau_levenshtein_distance(n1,n2)

    if hamm_trans > 4:
        return n1, n2
    else:
        final_1, final_2 = get_edit_distance(n1,n2,"ID")
        final_1 = trailing_space_symbol(final_1)
        final_2 = trailing_space_symbol(final_2)
        return final_1,final_2



def pair(s,star_indices):
    """

    :param s: a pair of records 
    :return: 
    """
    tmp1 = list(s[0])
    tmp2 = list(s[1])
    rec_1 = []
    rec_2 = []
    star_1 = []
    star_2 = []
    star_index_values = star_indices.values()
    for i in range(len(tmp1)):
        if i in star_index_values:
            if i == star_indices["dob"]:
                x, y = get_star_date(tmp1[i], tmp2[i])
            elif i == star_indices["voter_reg_num"]:
                x, y = get_star_vot_reg(tmp1[i], tmp2[i])
            elif i == star_indices["last_name"] or i == star_indices["first_name"]:
                if tmp1[star_indices["last_name"]] == tmp2[star_indices["first_name"]] and tmp2[star_indices["last_name"]] == tmp1[star_indices["first_name"]]:
                    x, y = tmp1[i], tmp2[i]
                    # name_swap = True
                elif check_starring(tmp1[i], tmp2[i]):
                    x, y = get_edit_distance(tmp1[i], tmp2[i])
                else:
                    x, y = tmp1[i], tmp2[i]
            elif i == star_indices["race"] or i == star_indices["sex"]:
                if tmp1[i] == tmp2[i]:
                    x, y = "*", "*"
                else:
                    x, y = tmp1[i], tmp2[i]
            else:
                x,y = tmp1[i], tmp2[i]
            rec_1 += [tmp1[i]]
            rec_2 += [tmp2[i]]
            star_1 += [x]
            star_2 += [y]

    return (rec_1 + star_1, rec_2 + star_2)

def find_index(name_list, prop_name):
    for i in range(len(name_list)):
        if (name_list[i].upper() == prop_name.upper()):
            return i

def make_list_dict(file_path,id_name):
    f = open(file_path, 'r')
    reader = csv.reader(f)
    d = {}
    tmp = []
    for row in reader:
        tmp += [row]
    title = tmp[0]
    tmp = tmp[1:len(tmp)]
    n = len(title)

    index_id = find_index(title, id_name)
    index_vot_reg = find_index(title, "voter_reg_num")
    index_fname = find_index(title, "first_name")
    index_lname = find_index(title, "last_name")
    index_dob = find_index(title, "dob")
    index_file_id = find_index(title,"file_id") -1
    star_calc_indexes = {"voter_reg_num":index_vot_reg-1, "last_name":index_lname-1,"first_name":index_fname-1,"dob":index_dob-1}
    star_calc_indexes["race"] = find_index(title,"race") -1
    star_calc_indexes["sex"] = find_index(title, "sex") - 1
    data = {}
    ff = {}
    lf = {}

    for r in range(len(tmp)):
        rec = tmp[r]
        id = rec[index_id]

        if rec[index_lname] not in lf:
            lf[rec[index_lname]] = 1
        else:
            lf[rec[index_lname]] += 1
        if rec[index_fname] not in ff:
            ff[rec[index_fname]] = 1
        else:
            ff[rec[index_fname]] += 1

        del rec[index_id]
        if(id not in data.keys()):
            data[id] = [rec]
        else:
            rec = data[id].append(rec)

    return data, title, star_calc_indexes, ff,lf, index_file_id

def star_similarities(d, star_indices,index_file_id,title):
    data = []
    # id = 1
    for p in d:
        for i in range(1, len(d[p])):
            file_id_1 = d[p][0][index_file_id]
            file_id_2 = d[p][i][index_file_id]
            type_1 = d[p][0][title.index("type")-1]
            type_2 = d[p][1][title.index("type")-1]
            answer_1 = d[p][0][title.index("same")-1]
            answer_2 = d[p][1][title.index("same")-1]
            ff_1 = d[p][0][title.index("cntfn") - 1]
            ff_2 = d[p][1][title.index("cntfn") - 1]
            lf_1 = d[p][0][title.index("cntln") - 1]
            lf_2 = d[p][1][title.index("cntln") - 1]
            # if not file_id_1 == file_id_2:
            x, y = pair([d[p][0], d[p][i]], star_indices)
            data += [[p, file_id_1] + x + [ff_1,lf_1,type_1,answer_1]]
            #print([[p, file_id_1] + x + [ff_1,lf_1,type_1,answer_1]])
            data += [[p, file_id_2] + y + [ff_2,lf_2,type_2,answer_2]]
            # id += 1
    return data

def data_filter(data_as_list,item):
    new_data = []
    for i in range(len(data_as_list)):
        if item in data_as_list[i]:
            new_data.append(data_as_list[i])
    return(new_data)

def get_col_indices(data, star_indices, order):
    id_grp = [0,1]
    len_array = len(data[0])
    type_answer = [len_array-2,len_array-1]
    org = [star_indices[item] + 2 for item in order]
    offset = (len(data[0]) - 2) / 2 - 1
    star =  [i + offset for i in org]
    all_indices = id_grp + org + star + type_answer
    return all_indices

def reorganize_cols(data, star_indices, order):
    col_indices = get_col_indices(data, star_indices, order)
    new_data = []
    for i in range(len(data)):
        rec = []
        for j in col_indices:
            rec.append(data[i][j])
        new_data.append(rec)
    return new_data

def write_data(data_list,file_name, title_array):
    f = open(file_name,'w')
    w = csv.writer(f)
    #w.writerow(title_array)
    for i in range(len(data_list)):
        # rec = data_list[i]
        # rec.insert(3, ff[rec[2]])
        # rec.insert(5, lf[rec[4]])
        # data_list[i] = rec
        w.writerow(data_list[i])
    f.close()


def pre_processing(pair_filename, name_frequency_file):
    # 1. count name frequency
    # 2. add same column to the end

    firstname = defaultdict(int)
    lastname = defaultdict(int)

    with open(name_frequency_file, 'r') as fin:
        for line in fin:
            row = line.strip().split(',')
            row = [r.strip(' ') for r in row]
            if row[0] == 'F':
                firstname[row[1]] += int(row[2])
            else:
                lastname[row[1]] += int(row[2])

    data = list()
    with open(pair_filename, 'r') as fin:
        i = 0
        for line in fin:
            if i == 0:
                data.append(line.rstrip('\n')+',cntfn,cntln,same'+'\n')
            else:
                row = line.rstrip('\n').split(',')
                fn = row[2].strip(' ')
                ln = row[3].strip(' ')

                cntfn = firstname[fn]
                cntln = lastname[ln]

                data.append(line.rstrip('\n')+','+str(cntfn)+','+str(cntln)+',0\n')
            i += 1

    with open(pair_filename, 'w+') as fout:
        for line in data:
            fout.write(line)


def post_processing(filename, out_filename):
    data = list()

    with open(filename, 'r') as fin:
        for line in fin:
            row = line.rstrip('\n').split(',')
            if len(row) == 18:
                data.append([row[0], row[2], row[14], row[3], row[4], row[15], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], 0, 0, 0])

    with open(out_filename, 'w+') as fout:
        for d in data:
            fout.write(','.join([str(x) for x in d]))
            fout.write('\n')


def generate_pair_file2(filename, name_frequency_file, out_filename):
    """
    filename: the input pair-file
    fileA: database A
    fileB: database B
    out_filename: result pair file
    """
    pre_processing(filename, name_frequency_file)

    d ,title, star_indices , ff, lf, index_file_id = make_list_dict(filename,"ID")
    print("The number of items in d are", len(d))
    print(title)
    print(star_indices)
    data = star_similarities(d, star_indices,index_file_id,title)
    print("The number of items in data are", len(data))
    # data_starred = reorganize_cols(data, star_indices, ["voter_reg_num","first_name", "last_name", "dob","sex","race"])
    title_array = [b'Group ID', b'Record ID',b'Reg No.',b'First Name', b'Last Name', b'DoB',b'Sex', b"Race", b'Reg No.',b'First Name', b'Last Name', b'DoB',b'Sex',b'Race',b'FF',b'LF',b'type',b'Same']
    write_data(data, out_filename, title_array)

    post_processing(out_filename, out_filename)

    info = {
        'size': len(data)/2
    }
    return info


def generate_fake_file(out_filename):
    data = list()

    with open('data/ppirl.csv', 'r') as fin:
        for line in fin:
            data.append(line)

    with open(out_filename, 'w+') as fout:
        for line in data:
            fout.write(line)


#generate_pair_file('data/sample.csv', 'data/test.csv')



