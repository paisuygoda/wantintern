import psycopg2
import pickle
import csv

with open('good_domain.pickle', mode='rb') as f:
    good_domain = pickle.load(f)

conn = psycopg2.connect("host=sync-messenger-qa-blue.crp2azrgxykc.ap-northeast-1.rds.amazonaws.com port=5432"
                        " dbname=hermes user=swanson password=3DQPWBmL2VeVMRuv")

cur = conn.cursor()

f = open('data_good_domain.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

for domain in good_domain:
    if domain == '@':
        continue

    cur.execute("select * from yashima_search_logs where strpos(emails, %s) > 0", [domain])
    data_in_domain = cur.fetchall()

    writer.writerows(data_in_domain)






cur.close()
conn.close()
f.close()