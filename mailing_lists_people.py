'''
MIGRATION 1:

Donusturulen tablo: "mailing_lists_people"

Bu donusum
--------------

* `MList` etiketli her mailing_list icin bir dugum olusturur.
* `:MUser` etiketli her kullanici icin bir dugum olusturur.
* Kullanıcıyı mailing_list'e baglar. `:BELONGS_TO`
* Diger dugumlere ekstra bilgi eklemez.


Not
----


Taşınan tablo bir many-to-many bağlantı tablosu olduğundan her düğümün özellik bilgileri içermez. 

'''

# Import MySQL-python conncetor
import _mysql

# Import py2neo (python connector for Neo4j)
from py2neo import Graph

db=_mysql.connect()

db = raw_input("Enter Database Name (Default: AmarokDB)") or "AmarokDB"
host = raw_input("Enter Host Name (Default: localhost)") or "localhost"
user = raw_input("Enter Username (Default: root)") or "root"
password = raw_input("Enter password (Default: <blank>)") or ""


db=_mysql.connect(host=host ,user=user, passwd=password, db=db)

db.query("""SELECT * FROM mailing_lists_people""")
result = db.use_result()

# MySQL veritabanındaki alanların adı(fields).
fields = [e[0] for e in result.describe()]

#MySQL tablosundaki satırların hepsini dondurur.
rows = result.fetch_row(maxrows=0)

# 2 alanımız var.
# (email_address, mailing_list_url)

# Calisan neo4j veri tabanina baglanır.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Filtreleme icin siklikla kullanilabilecek alanlarda index olusturur.
n4j_graph.cypher.execute("CREATE INDEX ON :MUser(email)")
n4j_graph.cypher.execute("CREATE INDEX ON :MList(mailing_list_url)")

ctr = 0
for row in rows:
    print row
    email = row[0]
    mailing_list_url = row[1]

    s = '''MERGE (u:MUser { %(primary_key_field)s: "%(email)s"})
           MERGE (m:MList { mailing_list_url: "%(mailing_list_url)s"})
           CREATE UNIQUE u-[:BELONGS_TO]->m'''%{"primary_key_field": fields[0], "email": email, "mailing_list_url": mailing_list_url }
    n4j_graph.cypher.execute(s)
