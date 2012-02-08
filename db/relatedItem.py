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


#add tag attribute of item table with tags attributes: (裙;热;高腰;可爱;) => (2;13,7,17)
def updateItemTag(dbsession):
    id = 594;
    item = dbsession.query(Item).filter(Item.id == id).first()
    tags = item.tag.strip().split(";") 
    for tag in tags:


def _union(leftU, rightU):
    unionObj = {}
    for item in leftU:
        if unionObj.has_key(item):
            unionObj[item] += 1
        else:
            unionObj[item] = 1
    for item in rightU:
        if unionObj.has_key(item):
            unionObj[item] += 1
        else:
            unionObj[item] = 1
    for key in unionObj.keys():
        if unionObj[key] != 2:
            del(unionObj[key])
    return len(unionObj.keys())
    
        

#main function, the entrance of the program
if __name__ == "__main__":
    #engine = create_engine(db_uri)
    #Session = sessionmaker(bind=engine)
    #session = Session()
    #updateItemTag(session)
