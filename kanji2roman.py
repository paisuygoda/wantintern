# coding: utf8
import csv
import pickle
from pykakasi import kakasi
from name_separator_svm import names_vectorize, svm_name, make_boc
import copy

vowels = ['a', 'i', 'u', 'e', 'o', '']
consonents = ['', 'k', 'ky', 'c', 'g', 's', 'sh', 'z', 'j', 't', 'ch', 'ts', 'd', 'n', 'ny', 'h', 'hy', 'b', 'by', 'p',
              'py', 'f', 'm', 'my', 'y', 'r', 'ry', 'l', 'w']

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


def count_roman_miss(f2):
    reader = csv.reader(f2)
    count = 0
    for row in reader:
        name = row[1]
        if isfullname(name):
            continue
        count += 1
    return count


def count_kanji_miss(f3):
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


def isfamilyname(fullroman, clf):
    data = []
    labels = []
    make_boc(fullroman, data, labels, False)
    if len(data) == 0:
        return False
    estimated_label = clf.predict(data)
    estimated_label = estimated_label[len(estimated_label)-1]
    if estimated_label == 0:
        return True
    return False


def roman_correction(roman_kanji_list):

    data, labels = names_vectorize()
    clf = svm_name(data, labels)

    for k, row in roman_kanji_list.items():
        roman = row[1]
        kanji = row[2]
        if isfullname(roman):
            continue
        kak = kakasi()
        kak.setMode('J', 'a')
        conv = kak.getConverter()
        familyname_length = 0
        for i in range(len(kanji)):
            familyname_candidate = kanji[:i+1]
            familyname_roman = conv.do(familyname_candidate)
            if isfamilyname(familyname_roman, clf):
                familyname_length = i+1
                break

        familyname = kanji[:familyname_length]
        firstname = kanji[familyname_length:]
        familyname_roman = conv.do(familyname)
        firstname_roman = conv.do(firstname)
        fullname = (familyname_roman + ' ' + firstname_roman).title()
        row[1] = fullname


def preprocessing_roman_correction(f, namerow):
    reader = csv.reader(f)
    roman_kanji = {}
    for row in reader:
        namelist = ripper(row[namerow])
        no_roman = True
        no_kana = True
        kanji = ''
        roman = ''
        for name in namelist:
            name = name.replace(' ', '')
            name = name.replace('　', '')
            if name.isalnum():
                if not isfullname(name):
                    no_roman= False
                roman = name
            elif iskana(name):
                if len(kanji) == 0:
                    no_kana = False
                    kanji = name
            elif len(name) > len(kanji) or iskana(kanji):
                no_kana = False
                kanji = name
        if no_roman or no_kana:
            continue
        kanji = kanji.decode('utf8')
        roman_kanji[row[0]] = [row[0], roman, kanji]

    return roman_kanji

f = open('dataset_mini_100.csv', 'r')
namelist = preprocessing_roman_correction(f, 5)
roman_correction(namelist)
f.close()
f = open('dataset_mini_100.csv', 'r')
reader = csv.reader(f)
fw = open('dataset_mini_100_corrected_name.csv', 'w')
writer = csv.writer(fw)
for row in reader:
    if namelist.has_key(row[0]):
        set = namelist[row[0]]
        s = '["' + set[1].encode('utf8') + '","' + set[2].encode('utf8') + '"]'
        row[5] = s

    writer.writerow(row)