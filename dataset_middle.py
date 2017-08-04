import psycopg2
import pickle
import csv

yaba_list = [
    '@',
    '["jp',
    '["email',
    '["mail',
    '["e-mai',
    '["e-mail',
    '["e-mail :',
    '["e-ma i',
    '["e-mail:',
    '["email:',
    '["mail:',
    '["e-ma',
    '["e mail',
    '"-mail"'
]
with open('good_domain.pickle', mode='rb') as f:
    good_domain = pickle.load(f)

conn = psycopg2.connect("host=sync-messenger-qa-blue.crp2azrgxykc.ap-northeast-1.rds.amazonaws.com port=5432"
                        " dbname=hermes user=swanson password=3DQPWBmL2VeVMRuv")

cur = conn.cursor()

f = open('data_good_domain_middle.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

for i, domain in enumerate(good_domain):
    if domain in yaba_list:
        continue
    cur.execute("select * from yashima_search_logs where id > 19000000 and strpos(emails, %s) > 0", [domain])
    data_in_domain = cur.fetchall()

    writer.writerows(data_in_domain)
    print('finished {0} / {1}'.format(i, len(good_domain)))




cur.close()
conn.close()
f.close()