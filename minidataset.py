# coding: utf8
import pickle
import csv
import random

original_dataset = 'data_good_domain_middle.csv'
output_file = 'dataset_mini_100.csv'


def minidata_pickle():

    f = open('data_good_domain_middle.csv', 'r')
    reader = csv.reader(f)
    listn = []
    listd = []
    with open('good_domain.pickle', mode='rb') as fgd:
        gd = pickle.load(fgd)
    for i, row in enumerate(reader):
        if not ('@' in row[8]):
            continue
        domain = row[8].split('@')
        if '"]' in domain[1]:
            domain1 = domain[1].split('"]')
        if '","' in domain1[0]:
            domain1 = domain1[0].split('","')
        domain = domain1[0]
        domain = '@' + domain
        if not (domain in gd):
            continue
        if row[0] in listn:
            continue
        listn.append(row[0])
        listd.append(row)

    return listd


def minidata100(listd):

    fw = open('data_good_domain_mini_100_3.csv', 'w')
    writer = csv.writer(fw)

    random.shuffle(listd)
    new_list = []
    for i, row in enumerate(listd):
        new_list.append(row)
        if len(new_list) == 100:
            break

    writer.writerows(new_list)

listd = minidata_pickle()
minidata100(listd)
