#!/usr/bin/env python
import ConfigParser
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

#veritabina baglanma
connection = "mysql://root:Password@127.0.0.1/mlistdata?charset=utf8"

#Baglanilan veritabanindan graph uretme
graph = create_schema_graph(metadata=Metadata(connection), show_datatypes=False, show_indexes=False, rankdir='LR', concentrate=False)

#Png resim uretme
graph.write_png('dbschema.png')
