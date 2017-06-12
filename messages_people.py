'''
MIGRATION 4:
Donusturulen tablo: "messages_people"

Bu donusum:

* Veritabanindaki her `Message`, `MUser` tarafindan gonderilir. Tum bu tur iliskileri yaratmak icin
messages_people tablosu kullanilir. Bu sekilde her ileti bir kullaici alir.
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

db.query("""SELECT * FROM messages_people""")
result = db.use_result()
fields = [e[0] for e in result.describe()]

# Tablodaki butun satırları dondurur.
rows = result.fetch_row(maxrows=0)

# Calisan neo4j veri tabanina baglanır.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Filtreleme icin siklikla kullanilabilecek alanlarda index olusturur.
n4j_graph.cypher.execute("CREATE INDEX ON :Message(%s)"%(fields[0],))

ctr = 0
for row in rows:

    #print row[1], row[2]
    email = row[0]
    mailing_list_url = row[1]

    properties = {}
    for col in range(len(fields)):
        properties[fields[col]] = row[col]
    n4j_properties = PropertySet(properties)

    s = '''MATCH (m:Message {message_ID: "%s"}), (u:MUser {email_address: "%s"})
           CREATE UNIQUE (m)-[:FROM]->(u)'''%(properties['message_id'],
                                                    properties['email_address'])
    print s
    n4j_graph.cypher.execute(s)
