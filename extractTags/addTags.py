#coding=utf-8

import datetime
import random

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
db_uri = "mysql+mysqldb://root:root@localhost:3306/wodfan_tag_2_0212?charset=utf8"

#data model mapping
class Item(Base):
    __tablename__ = "items"

    id = Column('item_id', Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(256))
    brand = Column(VARCHAR(64))
    pattern = Column(VARCHAR(32))
    description = Column(VARCHAR(2048))
    style = Column(VARCHAR(32))
    design = Column(VARCHAR(16))
    material = Column(VARCHAR(16))
    properties = Column(VARCHAR(1024))
    link = Column(VARCHAR(256))
    category = Column(Integer(5))     

    def __init__(self, id, title, brand, pattern, description, style, design, material, properties, link, category):
        self.id = id
        self.title = title
        self.brand = brand
        self.pattern = pattern 
        self.description = description
        self.style = style 
        self.design = design
        self.material = material 
        self.properties = properties 
        self.link = link
        self.category = category

class Tag(Base):
    __tablename__ = "tag"

    tag_id = Column('tag_id', Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(256))
    type = Column(Integer(11))

    def __init__(self, tag_id, name, type):
        self.tag_id = tag_id
        self.name = name
        self.type = type

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

class Category(Base):
    __tablename__ = "category"

    category_id = Column('category_id', Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer(5))
    name = Column(VARCHAR(32))

#baseCats = []

def getTags(dbsession):
    tags = dbsession.query(Tag)
    items = dbsession.query(Item)
    #temp = open('temp', 'w')
    seasons = [u'冷', u'暖'];
    for item in items:
        tagsDict= dict() 
        baseCats = '' 
        if item is not None and item.id is not None:
            addTagsDict(tagsDict, tags, item.brand) 
            addTagsDict(tagsDict, tags, item.pattern) 
            addTagsDict(tagsDict, tags, item.description) 
            addTagsDict(tagsDict, tags, item.style) 
            addTagsDict(tagsDict, tags, item.design) 
            addTagsDict(tagsDict, tags, item.material) 
            addTagsDict(tagsDict, tags, item.properties) 

            baseCategory = findBaseCategory(dbsession, item.category, baseCats)
            print baseCats
            currentSeason = seasons[random.randint(0, 1)]

            finalTags = []
            finalTags.append(baseCategory)
            finalTags.append(currentSeason)
            
            #print '>>>>>>>>>>>>>>>>>>>>>>>>>>>' + baseCategory + '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' +'\n'

            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(item.id) + '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' +'\n'
            print ';'.join(tagsDict.keys())
            
            colorFilter(tags, tagsDict, finalTags)
            
            for k in tagsDict.keys():
                if k != baseCategory and not isConflict(baseCategory, k, baseCats):
                   finalTags.append(k) 

            #print '****************************************************************************' + '\n'  
            finalTags = ';'.join(finalTags)
            print finalTags
             
            sql = 'update items set tags="' + finalTags + '" where item_id=' + str(item.id)
            dbsession.execute(sql)
            #temp.writelines('update items set tags="' + finalTags + '" where item_id=' + str(item.id)) 
            #item.tags = finalTags
            #dbsession.add(item)
            #dbsession.flush()

def colorFilter(tags, tagsDict, finalTags):  
    for k in tagsDict.keys():
        if k.find(u'色') != -1:
            for tag in tags:
                if tag.type == 0:
                    #print tag.name + ":" + k 
                    if tag.name == k:
                        print ">>>>>>" + k
                        finalTags.append(k)
                        del tagsDict[k]

def isConflict(inBaseCat, judgeTag, baseCats):    
    f = False
    for baseCat in baseCats:
        #print judgeTag + ":" + baseCat.name + "\n"
        if judgeTag.find(baseCat.name) != -1:
            f = True
            break
    return f

def addTagsDict(dict, tags, searchString):
    if searchString:
        for tag in tags:
            if searchString.find(tag.name) != -1:
                if not dict.has_key(tag.name):
                    dict[tag.name] = 1
                else:
                    dict[tag.name] += 1

def findBaseCategory(dbsession, category_id, baseCats):
    res = ""
    #global baseCats
    childCat =  dbsession.query(Category).filter(Category.category_id == category_id).first()
    if childCat and childCat.parent_id:
        parentCat = dbsession.query(Category).filter(Category.category_id == childCat.parent_id).first()
        if parentCat and parentCat.name:
            res = parentCat.name
            baseCats = dbsession.query(Category).filter(Category.parent_id == 0).filter(Category.name != parentCat.name).all()
    return res
                        
#main function, the entrance of the program
if __name__ == "__main__":
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    getTags(session)
    session.commit()
