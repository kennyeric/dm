# -*- coding: utf-8 -*-

import datetime

#sqlalchemy common lib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float

from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from sqlalchemy.ext.declarative import declarative_base

#sqlalchemy lib for mysql dialect
from sqlalchemy.dialects.mysql import VARCHAR,DATETIME

#Base class for mapping data model
Base = declarative_base()

#mysql db's uri
db_uri = "mysql+mysqldb://root:root@localhost:3306/wodfan_tag?charset=utf8"

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
    tag = Column(VARCHAR(2048))
    old_id = Column(Integer)
    url = Column(VARCHAR(256))
    review = Column(Integer)

    def __init__(self, tags, link, source, source_id, title, description, publish_date, tag, old_id, url, review):
        self.tags = tags
        self.link = link
        self.source = source
        self.source_id = source_id
        self.title = title
        self.description = description
        self.publish_date = publish_date
        self.tag = tag 
        self.old_id = old_id
        self.url = url
        self.review = review

    def __repr__(self):
        return "<Item('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.tags, self.link, self.source, self.source_id, self.title, self.description, self.publish_date, self.tag, self.old_id, self.url, self.review)

class RelationTag(Base):
    __tablename__ = "relation_tag"

    id = Column('relation_tag_id', Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    target_id = Column(Integer)
    relation = Column(Float, ColumnDefault(0.5))

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
    type = Column(Integer)

    def __init__(self, name, pinyin, type):
        self.name = name
        self.pinyin = pinyin 
        self.type = type

    def __repr__(self):
        return "<Tag('%s', '%s')>" % (self.name, self.pinyin, self.type)

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
                print "mongodb: insert ('%s', '%s') item to %s" % (item.id, mongodb_tags, mgsession)
                mgsession["item"].insert({"item_id": item.id, "tags": mongodb_tags})

def tag2id(tagname, dbsession):
    tagRow = dbsession.query(Tag).filter(Tag.name == tagname).first()
    id = -1
    if tagRow:
        if tagRow.id:
            id = tagRow.id
        return id
    else:
        return id

#add tag attribute of item table with tags attributes: (裙;热;高腰;可爱;) => (2;13,7,17)
def updateItemTag(dbsession):
    items = dbsession.query(Item)
    for item in items:
        tagsString = item.tags.strip()
        if tagsString:
            tagsString = tagsString[0:len(tagsString) - 1]
            tags = tagsString.split(";") 
            tagIDs = ""
            for tag in tags:
                tagItem = dbsession.query(Tag).filter(Tag.name == tag).first();
                tagIDs += str(tagItem.id) + ";"
            tagIDs = tagIDs[0:len(tagIDs) - 1]
            print tagIDs + "<==>" + str(item.id)
            dbsession.execute('update item set tag=:tag where item_id=:id', {"tag":tagIDs, "id":item.id})

#main function, the entrance of the program
if __name__ == "__main__":
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    updateItemTag(session)
