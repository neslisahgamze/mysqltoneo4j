'''
MIGRATION 2:

Donusturulen tablo : "messages"

Bu donusum
--------------
* `Message` etiketli her message icin dugum olusturur.
* MList ile message dugumlerini iliskilendirir.`:BELONGS_TO`
  Yani, Message BELONGS_TO MList

* Message onlari gonderen kisilerle hala iliskili degil, cunku henuz people iliskisini
kullanilmadi, diger donusumde kullanilacak.
'''

# Import MySQL-python conncetor
import _mysql

# Import py2neo (python connector for Neo4j)
from py2neo import Graph, PropertySet, rel, Path
from py2neo.cypher import MergeNode

db=_mysql.connect()

db = raw_input("Enter Database Name (Default: AmarokDB)") or "AmarokDB"
host = raw_input("Enter Host Name (Default: localhost)") or "localhost"
user = raw_input("Enter Username (Default: root)") or "root"
password = raw_input("Enter password (Default: <blank>)") or ""

db=_mysql.connect(host=host ,user=user, passwd=password, db=db)

db.query("""SELECT * FROM messages""")
result = db.use_result()
fields = [e[0] for e in result.describe()]

# Bu data icin ilk kolon message_ID.
assert fields[0] == 'message_ID'

#Tablodaki butun sutunlari donduruyoruz
rows = result.fetch_row(maxrows=0)


# Calisan neo4j veri tabanina baglanır.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Filtreleme icin siklikla kullanilabilecek alanlarda index olusturur.
n4j_graph.cypher.execute("CREATE INDEX ON :Message(%s)"%(fields[0],))

ctr = 0
for row in rows:

    email = row[0]
    mailing_list_url = row[1]

    properties = {}
    for col in range(len(fields)):
        properties[fields[col]] = row[col]
    n4j_properties = PropertySet(properties)

    # Islem
    tx = n4j_graph.cypher.begin()
    merge = MergeNode("Message", "message_ID", properties["message_ID"]).set(n4j_properties)
    tx.append(merge)
    tx.commit()

    s = '''MATCH (m:Message {message_ID: "%s"}), (l:MList {mailing_list_url: "%s"})
           CREATE UNIQUE (m)-[:BELONGS_TO]->(l)'''%(properties['message_ID'],
                                                    properties['mailing_list_url'])
    n4j_graph.cypher.execute(s)