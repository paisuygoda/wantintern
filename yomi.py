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
    a = [ch for ch in s if u"あ" <= ch <= u"ん"]
    if len(s) == len(a):
        return True
    return False


def hassymbol(s):
    kigou = [':', ',', '-', u'。', u'、', u'『', u'■', '.', '{', '/', '_', '(', u'「', u'¥', '|', u'·', u'」', 'L', '\'',
             u'□', '*', '#', '+']
    for a in s:
        if a in kigou:
            return True
    return False


def removesymbols(s):
    s = s.decode('utf8')
    kigou = [':', ',', '-', u'。', u'、', u'『', u'■', '.', '{', '/', '_', '(', u'「', u'¥', '|', u'·', u'」', 'L', '\'',
             u'□', '*', '#', '+']
    for k in kigou:
        s = s.replace(k, '')
    s = s.replace(u'　', ' ')
    return s


def split_fullname(s):
    pos = 0
    for i, c in enumerate(s):
        if 'A' <= c <= 'Z' and i > 0:
            pos = i

    first = s[:pos]
    family = s[pos:]
    return [first, family]


def isfullname(s):
    a = [ch for ch in s if "A" <= ch <= "Z"]
    if len(a) == 2:
        return True
    return False


def make_namelist():

    f = open('data_good_domain_middle.csv', 'r')
    reader = csv.reader(f)
    l = []
    for row in reader:
        names = ripper(row[5])
        no_alpha = True
        no_hiragana = True
        kanji = ''
        roman = ''
        for name in names:
            name = removesymbols(name)
            if name.encode('utf8').isalnum() and isfullname(name):
                no_alpha = False
                roman = split_fullname(name)
            elif iskana(name):
                if len(kanji) == 0:
                    no_hiragana = False
                    kanji = name
            elif len(name) > len(kanji) or iskana(kanji):
                no_hiragana = False
                kanji = name
        if no_alpha or no_hiragana or not(2 < len(kanji) < 7):
            continue
        t = [roman, kanji]
        l.append(t)

    with open('namelist.pickle', mode='wb') as nl:
        pickle.dump(l, nl)


def make_annotation():
    with open('yomi_annotation.pickle', mode='rb') as fa:
        annotation = pickle.load(fa)
    with open('annotation_num.pickle', mode='rb') as an:
        zenkai = pickle.load(an)
    with open('namelist.pickle', mode='rb') as nl:
        namelist = pickle.load(nl)

    count = 0
    pause_annotation = False

    for name in namelist:
        count += 1
        if count <= zenkai:
            continue
        print name[0][1] + ' ' + name[0][0]
        print name[1]
        tag = raw_input()
        if '0' <= tag <= '9':
            tag = int(tag)
            family = name[1][:tag]
            first = name[1][tag:]
            name[1] = [first, family]
            annotation.append(name)
            print family
        elif tag == 'q':
            pause_annotation = True
        elif tag == 'b':
            pause_annotation = True
            annotation.pop()
            count -= 1
        elif tag == 'r':
            mid = name[0][0]
            name[0][0] = name[0][1]
            name[0][1] = mid
            print name[0][1] + ' ' + name[0][0]
            print name[1]
            tag = raw_input()
            if '0' <= tag <= '9':
                tag = int(tag)
                family = name[1][:tag]
                first = name[1][tag:]
                name[1] = [first, family]
                annotation.append(name)

        if pause_annotation:
            count -= 1
            break

    with open('annotation_num.pickle', mode='wb') as an:
        pickle.dump(count, an)

    with open('yomi_annotation.pickle', mode='wb') as fa:
        pickle.dump(annotation, fa)

#make_namelist()
#make_annotation()
