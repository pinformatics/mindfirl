import json


def load_data_from_csv(filename):
    data = list()
    filein = open(filename, 'r')
    for line in filein:
        record = line.split(',')
        data.append(record)
    return data
