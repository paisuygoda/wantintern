# coding: utf8
import pickle
import csv
import psycopg2
import random
import Levenshtein


def see_pickle():

    with open('yomi_annotation.pickle', mode='rb') as f:
        gd = pickle.load(f)
    for names in gd:
        print names[0][1] + ' ' + names[0][0]
        print names[1][1] + ' ' + names[1][0]


def good_domain_exile_blacklist():
    with open('good_domain.pickle', mode='rb') as f:
        gd = pickle.load(f)
    with open('existing_domain.pickle', mode='rb') as f2:
        ed = pickle.load(f2)
    for domain in gd:
        if domain not in ed:
            gd.remove(domain)
            continue


    with open('good_domain_leftover.pickle', mode='wb') as f:
        pickle.dump(gd, f)

def see_id():
    f = open('dataset_mini_100_corrected.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        print (row[1]+'\t'+row[4]+'\t'+row[5]+'\t'+' '+'\t'+row[7]+'\t'+row[6]+'\t'+row[7])

def see_ida():
    f = open('dataset_mini_100_answer.csv', 'r')
    reader = csv.reader(f)
    l = []
    for row in reader:
        row = ripper(row[2])
        for r in row:
            print r
        print '----------'
    f.close()

    with open('existing_domain.pickle', mode='wb') as f:
        pickle.dump(l, f)


def ranselegd():
    with open('gd_data.pickle', mode='rb') as f:
        gd = pickle.load(f)

    for i in gd:
        print i


def cut(word):
    mid = word.split('"')
    if len(mid) > 1:
        word = mid[1]
    else:
        word = mid[0]
    return word


def ripper(a):
    a = a.split('["')
    if len(a)>1:
        a = a[1].split('"]')
    else:
        a = a[0].split('"]')
    return a[0].split('","')


def make_answer_csv():
    f = open('ma.csv', 'r')
    reader = csv.reader(f)
    l = []
    go = False
    for row in reader:
        if not (row[1] == '19018414' or go):
            continue
        go = True
        if row[1] == '19038323':
            go = False

        l.append(row)

    f.close()
    fw = open('dataset_mini_100_answer.csv', 'w')
    writer = csv.writer(fw)
    writer.writerows(l)


def get_domains():
    with open('good_domain.pickle', mode='rb') as f:
        gd = pickle.load(f)
    f = open('dataset_mini_100_answer.csv', 'r')
    reader = csv.reader(f)

def reset_annotation():

    annotation = []
    count = 0

    #with open('yomi_annotation.pickle', mode='wb') as fa:
    #    pickle.dump(annotation, fa)
    with open('annotation_num.pickle', mode='wb') as an:
        pickle.dump(count, an)

see_pickle()