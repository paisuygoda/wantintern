# coding: utf8
import csv
import pickle
import copy
from sklearn import datasets
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
import random

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


def throwin_kana(bag, kana, name, l, c):
    if bag.has_key(kana):
        bag[kana] += 1
    else:
        if bag.has_key(name[l]):
            bag[name[l]] += 1
        kana = name[l + 1:c]
        return throwin_kana(bag, kana, name, l+1, c)

    return bag


def make_boc(name, data, labels, train=True):

    boc = {}
    for c in consonents:
        for v in vowels:
            boc[c+v] = 0

    last_vowel = 0
    for i, char in enumerate(name):
        if char in vowels:
            pos = i + 1
            if last_vowel == 0:
                kana = name[:pos]
                if boc.has_key(kana):
                    boc[kana] += 1
            else:
                kana = name[last_vowel:pos]
                throwin_kana(boc, kana, name, last_vowel, pos)
            last_vowel = pos
            if pos == len(name) and train:
                append_vector(boc, 0, data, labels)
            else:
                if random.random() < 0.3:
                    append_vector(boc, 1, data, labels)


def append_vector(boc, label, data, labels):
    vec = []
    for c in consonents:
        for v in vowels:
            vec.append(boc[c + v])
    data.append(vec)
    labels.append(label)


def names_vectorize():
    with open('yomi_annotation.pickle', mode='rb') as ya:
        annotation = pickle.load(ya)

    data = []
    labels = []
    for fullname in annotation:
        family = fullname[0][1].lower()
        make_boc(family, data, labels)

        first = fullname[0][0].lower()
        make_boc(first, data, labels, False)

    return data, labels


def svm_name(data, labels):
    X = data
    y = labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    clf = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape=None, degree=3, gamma=0.001, kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    clf.fit(X_train, y_train)

    y_true, y_pred = y_test, clf.predict(X_test)
    print 'SVM Accuracies:'
    print classification_report(y_true, y_pred)

    return clf

data, labels = names_vectorize()
#clf = svm_name(data, labels)


