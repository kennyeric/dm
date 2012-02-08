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
db_uri = "mysql+mysqldb://root:root@localhost:3306/wodfan_tag_1?charset=utf8"

#data model mapping
class Item(Base):
    __tablename__ = "items"

    id = Column('item_id', Integer, primary_key=True, autoincrement=True)
    link = Column(VARCHAR(256))

    def __init__(self, id, link):
        self.id = id
        self.link = link

class Images(Base):
    __tablename__ = "images"

    image_id = Column('image_id', Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(256))
    position =  Column(Integer(11))

    def __init__(self, image_id, url, position):
        self.image_id = image_id
        self.url = url
        self.position = position

class ItemImage(Base):
    __tablename__ = "item_image"

    def __init__(self, item_image_id, item_id, image_id):
        self.item_image_id = item_image_id
        self.item_id = item_id
        self.image_id = image_id

    item_image_id = Column('item_image_id', Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer(11))
    image_id = Column(Integer(11))

def addLink(dbsession):
    items = dbsession.query(Item)
    outfile = open("addlink.sql", "w")
    for item in items:
        if item is not None:
            if item.id is not None: 
                ii = dbsession.query(ItemImage).filter(ItemImage.item_id == item.id).first()
                ims = dbsession.query(Images).filter(Images.image_id == ii.image_id).all()
                for im in ims: 
                    if im.position == 0:
                        print "item id : " + str(item.id)
                        print " image url : " + im.url
                        sql = "update items set link = '" + im.url + "' where item_id = " + str(item.id) + "\n" 
                        outfile.write(sql)

#main function, the entrance of the program
if __name__ == "__main__":
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    addLink(session)
