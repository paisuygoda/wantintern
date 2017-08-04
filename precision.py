# coding: utf8
import csv
import Levenshtein
import numpy as np

answer_csv = 'dataset_mini_100_answer.csv'
ans_id = 1
ans_name = 2
ans_company = 3
ans_email = 6
ans_phone = 7

test_csv = 'dataset_mini_100_corrected_name.csv'
test_id = 0
test_name = 5
test_company = 6
test_email = 8
test_phone = 7


def ripper(a):

    a = a.split('["')
    if len(a) > 1:
        a = a[1].split('"]')
    else:
        a = a[0].split('"]')
    return a[0].split('","')


def iskana(s):
    s = s.decode('utf-8')
    a = [ch for ch in s if u"あ" <= ch <= u"ん"]
    if len(s) == len(a):
        return True
    return False


def no_kana(l):
    for r in l:
        if iskana(r):
            l.remove(r)
    return l


def make_ans_dict():

    fd = open(answer_csv, 'r')
    readerd = csv.reader(fd)
    answerd = {}
    for row in readerd:
        ans_block = {}
        hash_id = row[ans_id]
        ans_block['name'] = no_kana(ripper(row[ans_name]))
        ans_block['company'] = ripper(row[ans_company])
        email_list = []
        m = ripper(row[ans_email])
        for candidate in m:
            if '@' in candidate:
                email_list.append(candidate)
        ans_block['email'] = email_list
        ans_block['phone'] = ripper(row[ans_phone])
        answerd[hash_id] = ans_block

    return answerd


def lev_dist(aa, bb):
    d = np.array([0.0, 0.0])
    for b in bb:
        b = b.decode('utf-8')
        min_d = 9999
        for a in aa:
            a = a.decode('utf-8')
            d = Levenshtein.distance(a, b)
            if d < min_d:
                min_d = d

        score = 100
        score -= 25 * min_d
        if min_d > 2:
            score = 0
            
        if min_d == 0:
            cm = 100
        else:
            cm = 0

        d += np.array([float(score), float(cm)])

    d /= len(bb)

    return [float(score), float(cm)]


def edit_distance_all(n, c, e, p, ans):
    d = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    count = 0
    if len(ans['name']) > 0:
        inc = lev_dist(n, ans['name'])
        d[0] += inc
        d[1] += inc
        count += 1
    if len(ans['company']) > 0:
        inc = lev_dist(c, ans['company'])
        d[0] += inc
        d[2] += inc
        count += 1
    if len(ans['email']) > 0:
        inc = lev_dist(e, ans['email'])
        d[0] += inc
        d[3] += inc
        count += 1
    if len(ans['phone']) > 0:
        inc = lev_dist(p, ans['phone'])
        d[0] += inc
        d[4] += inc
        count += 1
    d[0] /= count
    return d


answers = make_ans_dict()

f = open(test_csv, 'r')
reader = csv.reader(f)
rate = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
count = 0
for row in reader:
    count += 1
    if not (row[test_id] in answers):
        print("ERROR id {0} does not exist in answer data".format(row[test_id]))
        continue
    name = row[test_name]
    company = row[test_company]
    email = row[test_email]
    phone = row[test_phone]

    name = ripper(name)
    company = ripper(company)
    email_list = []
    m = ripper(email)
    for candidate in m:
        if '@' in candidate:
            email_list.append(candidate)
    email = email_list
    phone = ripper(phone)

    answer = answers[row[test_id]]
    inc = edit_distance_all(name, company, email, phone, answer)
    rate += inc

rate /= count

print 'score based on distance       : ' + str(rate[0][0])
print '    name    : ' + str(rate[1][0])
print '    company : ' + str(rate[2][0])
print '    email   : ' + str(rate[3][0])
print '    phone   : ' + str(rate[4][0])
print 'score based on complete match : ' + str(rate[0][1])
print '    name    : ' + str(rate[1][1])
print '    company : ' + str(rate[2][1])
print '    email   : ' + str(rate[3][1])
print '    phone   : ' + str(rate[4][1])






