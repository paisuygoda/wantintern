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
             u'□', '*', '#', '+', ' ', u'　']
    for k in kigou:
        s = s.replace(k, '')
    return s

def make_namelist():

    f = open('data_good_domain_middle.csv', 'r')
    reader = csv.reader(f)
    l = []
    for row in reader:
        names = ripper(row[5])
        for name in names:
            name = removesymbols(name)
            if len(name) < 4 and not (name.encode('utf8').isalnum() or iskana(name) or hassymbol(name)):
                l.append(name)
    with open('namelist.pickle', mode='wb') as nl:
        pickle.dump(l, nl)


def make_annotation():
    with open('fullname_annotation.pickle', mode='rb') as fa:
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
        print name
        tag = raw_input()
        if tag == '1' or tag == '2':
            tag = int(tag) - 1
            annotation.append((name, tag))
        elif tag == 'q':
            pause_annotation = True
        elif tag == 'b':
            pause_annotation = True
            annotation.pop()
            count -= 1

        if pause_annotation:
            count -= 1
            break

    with open('annotation_num.pickle', mode='wb') as an:
        pickle.dump(count, an)

    with open('fullname_annotation.pickle', mode='wb') as fa:
        pickle.dump(annotation, fa)

make_annotation()
