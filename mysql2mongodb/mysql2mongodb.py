import datetime

#sqlalchemy common lib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer

from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from sqlalchemy.ext.declarative import declarative_base

#sqlalchemy lib for mysql dialect
from sqlalchemy.dialects.mysql import VARCHAR,DATETIME

#pymongodb lib
from gridfs import GridFS
import pymongo

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

class RelationTag(Base):
    __tablename__ = "relation_tag"

    id = Column('relation_tag_id', Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    target_id = Column(Integer)
    relation = Column(Integer, ColumnDefault(1))

    def __init__(self, source_id, target_id, relation):
        self.source_id = source_id
        self.target_id = target_id
        self.relation = relation

    def __repr__(self):
        return "<RelationTag('%s', '%s', '%s')>" % (self.source_id, self.target_id, self.relation)

class Tag(Base):
    __tablename__ = "tag"

    id = Column('tag_id', Integer,primary_key=True,autoincrement=True)
    name = Column(VARCHAR(32))
    pinyin = Column(VARCHAR(128))

    def __init__(self, name, pinyin):
        self.name = name
        self.pinyin = name

    def __repr__(self):
        return "<Tag('%s', '%s')>" % (self.name, self.pinyin)

#mongodb initialize
def create_mongodb_session():
    db_uri = "mongodb://localhost:27017/" 
    db_name = "wodfan" 
    conn = pymongo.Connection(db_uri)
    return conn[db_name]

#global func, export mysql data to mongodb
def exportdb(dbsession, mgsession):
    items = dbsession.query(Item).limit(10)
    for item in items:
        tagsString = item.tags.strip()
        tagsString = tagsString[0:len(tagsString) - 1]
        if tagsString != "":
            tags = tagsString.split(";")
            mongodb_tags = []
            for tag in tags:
                mongodb_tags.append(tag2id(tag, dbsession))
                mgsession.db["item"].insert({"item_id": item.id, "tags": mongodb_tags})

def tag2id(tagname, dbsession):
    tagRow = dbsession.query(Tag).filter(Tag.name == tagname).first()
    id = -1
    if tagRow:
        if tagRow.id:
            id = tagRow.id
        return id
    else:
        return id

#main function, the entrance of the program
if __name__ == "__main__":
    mgsession = create_mongodb_session() 
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    exportdb(session, mgsession)

