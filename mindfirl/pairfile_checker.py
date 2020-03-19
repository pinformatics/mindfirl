import sys

filename = 'pairs.csv'

def is_digit(d):
    return ('0' <= d and d <= '9')

def is_valid_date(d):
    if len(d) != 10:
        return False
    if d[2] != '/' or d[5] != '/':
        return False
    idx = [0,1,3,4,6,7,8,9]
    for i in idx:
        if not is_digit(d[i]):
            return False
    return True

message = []
cnt = 0
with open(filename, 'r') as f:
    for line in f:
        if line:
            data = line.strip().split(',')
            if len(data) != 15:
                message.append('Line %d: incorrect column number.' % cnt)
                continue
            if cnt > 0:
                pairID = data[0]
                groupID = data[1]
                DB = data[2]
                ID = data[3]
                reg_num = data[4]
                DoB = data[7]

                col_id = [0,1,3,4]
                for j in col_id:
                    if not data[j].isnumeric():
                        message.append('Line %d, Column %d: Number expected.' % (cnt, j+1))
                if not is_valid_date(DoB):
                    message.append('Line %d, Column %d: Incorrect date format.' % (cnt, 8))
        cnt += 1

if len(message) == 0:
    message.append('Success!')

for item in message:
    print(item)
