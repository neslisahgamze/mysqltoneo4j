'''
MIGRATION 3:

Donusturulen tablo: "people"

Bu donusum migration1'deki mailinglist_people haritalanmasi kullanilarak olusturulan  MUser'dan faydalanir ve data fazla veri ekler.

* Her bir`MUser` attribute icin daha fazla bilgi ekler. (Insan veritabanindaki her kayit MUser dugume karsilik gelir.)


* Message hala onu gonderen kisiyle iliskilendirilmedi (People), cunku henuz people ilişkisi kullanilmadi,
sonraki donusumde kullanilacak.
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

db.query("""SELECT * FROM people""")
result = db.use_result()
fields = [e[0] for e in result.describe()]

# Tablodaki butun satirlari dondurur.
rows = result.fetch_row(maxrows=0)

# Calisan neo4j veri tabanina baglanır.
n4j_graph = Graph("http://localhost:7474/db/data/")

# Filtreleme icin siklikla kullanilabilecek alanlarda index olusturur.
n4j_graph.cypher.execute("CREATE INDEX ON :Message(%s)"%(fields[0],))

ctr = 0
for row in rows:

    print row[0]
    email = row[0]
    mailing_list_url = row[1]

    properties = {}
    for col in range(len(fields)):
        properties[fields[col]] = row[col]
    n4j_properties = PropertySet(properties)

    # Islem
    tx = n4j_graph.cypher.begin()
    merge = MergeNode("MUser", "email_address", properties["email_address"]).set(n4j_properties)
    tx.append(merge)
    tx.commit()

