# coding: utf8
import csv
import pickle


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


def isfullname(s):
    a = [ch for ch in s if "A" <= ch <= "Z"]
    if len(a) == 2:
        return True
    return False


def removesymbols(s):
    s = s.decode('utf8')
    kigou = [':', ',', '-', u'。', u'、', u'『', u'■', '.', '{', '/', '_', '(', u'「', u'¥', '|', u'·', u'」', 'L', '\'',
             u'□', '*', '#', '+', ' ', u'　']
    for k in kigou:
        s = s.replace(k, '')
    return s


def create_roman_kanji_pickle():
    f = open('data_good_domain_middle.csv', 'r')
    reader = csv.reader(f)
    name_correspond = []
    for row in reader:
        # name_list = ripper(row[2])
        name_list = ripper(row[5])
        noAlpha = True
        noHiragana = True
        kanji = ''
        for name in name_list:
            name = name.replace(' ', '')
            name = name.replace('　', '')
            if name.isalnum():
                noAlpha = False
                roman = name
            elif iskana(name):
                if len(kanji) == 0:
                    noHiragana = False
                    kanji = name
            elif len(name) > len(kanji):
                noHiragana = False
                kanji = name
        if noAlpha or noHiragana:
            continue
        t = (row[0], roman, kanji)
        name_correspond.append(t)

    fw = open('roman_kanji.csv', 'w')
    writer = csv.writer(fw)
    writer.writerows(name_correspond)
    fw.close()

    for i in name_correspond:
        print (i[1] + " : " + i[2])


def detect_roman_miss(f2):
    reader = csv.reader(f2)
    count = 0
    for row in reader:
        name = row[1]
        if isfullname(name):
            continue
        count += 1
    return count

def detect_kanji_miss(f3):
    reader = csv.reader(f3)
    count = 0
    for row in reader:
        name = row[2].decode('utf8')
        if 2 < len(name) < 7:
            continue
        count += 1
    return count

def make_popular_kanji_dict(f3):
    reader = csv.reader(f3)
    kanji_dict = {}
    for row in reader:
        name = row[2].decode('utf8')
        name = list(name)
        for ji in name:
            if ji not in kanji_dict:
                kanji_dict[ji] = 1
            else:
                kanji_dict[ji] += 1

    popular_kanji_list = []
    for ji in kanji_dict:
        if kanji_dict[ji] > 10:
            popular_kanji_list.append(ji)

    final_dict = {}
    for i, ji in enumerate(popular_kanji_list):
        final_dict[ji] = i

    with open('popular_kanji_dict.pickle', mode='wb') as pk:
        pickle.dump(final_dict, pk)

f = open('roman_kanji.csv', 'r')
total_count = 0
subcount = 0
reader = csv.reader(f)
partial = []
for row in reader:
    total_count += 1
    roman = row[1]
    kanji = row[2].decode('utf8')
    if not (isfullname(roman) and 2 < len(kanji) < 7):
        print roman
        print kanji
        print 'https://m-api.wantedly.com/admin/yashima/search_logs/' + row[0]
