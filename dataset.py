import psycopg2
import pickle

conn = psycopg2.connect("host=sync-messenger-qa-blue.crp2azrgxykc.ap-northeast-1.rds.amazonaws.com port=5432"
                        " dbname=hermes user=swanson password=3DQPWBmL2VeVMRuv")

cur = conn.cursor()

cur.execute("select case when strpos(emails, '\",\"') = '0' and -strpos(emails, '@') + strpos(emails, '\"]') > 0 "
            "then substr( emails, strpos(emails,'@'),  -strpos(emails, '@') + strpos(emails, '\"]')) "
            "when -strpos(emails, '@') + strpos(emails, '\",\"') > 0 "
            "then substr( emails, strpos(emails,'@'),-strpos(emails, '@') + strpos(emails, '\",\"')) "
            "else null end as domain, count(*) from yashima_search_logs where id < 5000 group by domain;")


a = cur.fetchall()
good_domain = []

for aa in a:
    if aa[1] > 100:
        if aa[0]==None or aa[0] == '@gmail.com':
            continue
        good_domain.append(aa[0])

for i in good_domain:
    print(i)

# 連続でデータベース全体を見るのもアレなので、100以上あるドメインの獲得までで一旦止める

with open('good_domain.pickle', mode='wb') as f:
    pickle.dump(good_domain,f)

cur.close()
conn.close()