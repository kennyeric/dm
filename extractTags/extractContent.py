#coding=utf-8

import datetime

#sqlalchemy common lib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer

from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from sqlalchemy.ext.declarative import declarative_base

#sqlalchemy lib for mysql dialect
from sqlalchemy.dialects.mysql import VARCHAR,DATETIME

#Base class for mapping data model
Base = declarative_base()

#mysql db's uri
db_uri = "mysql+mysqldb://root:root@localhost:3306/wodfan_dev?charset=utf8"

#data model mapping
class Item(Base):
    __tablename__ = "item"

    id = Column('item_id', Integer, primary_key=True, autoincrement=True)
    tags = Column(VARCHAR(2048))
    link = Column(VARCHAR(256))
    source = Column(VARCHAR(256))
    source_id = Column(VARCHAR(512), ColumnDefault(""))
    title = Column(VARCHAR(1024))
    description = Column(VARCHAR(1024))
    publish_date = Column(DATETIME, ColumnDefault(datetime.datetime.now()))

    def __init__(self, tags, link, source, source_id, title, description, publish_date):
        self.tags = tags
        self.link = link
        self.source = source
        self.source_id = source_id
        self.title = title
        self.description = description
        self.publish_date = publish_date

    def __repr__(self):
        return "<Item('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.tags, self.link, self.source, self.source_id, self.title, self.description, self.publish_date)

#global func, export mysql content and description columns into a temp file 
def exportdb(dbsession):
    items = dbsession.query(Item)
    outfile_title = open("title", "w")
    outfile_content = open("content", "w") 
    for item in items:
        if item is not None:
            if item.title is not None:
                outfile_title.write(item.title.encode("utf8"));
            if item.description is not None: 
                outfile_content.write(item.description.encode("utf8"));

#main function, the entrance of the program
if __name__ == "__main__":
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    exportdb(session)

