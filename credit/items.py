#coding:utf-8

from scrapy.item import Item, Field

class PersonMore(Item):
    cid = Field()
    name = Field()
    caseCode = Field()
    age = Field()
    sex = Field()
    #focusNumber = Field()
    cardNum = Field()
    courtName = Field()
    areaName = Field()
    partyTypeName = Field()
    gistId = Field()
    regDate = Field()
    gistUnit = Field()
    duty = Field()
    performance = Field()
    disruptTypeName = Field()
    publishDate = Field()
    detailLink = Field()
    def __init__(self, item = None):
        if item == None:
            Item.__init__(self)
            self['cid'] = 0
            self['name'] = ""
            self['caseCode'] = ""
            self['age'] = ""
            self['sex'] =  ""
            #self['focusNumber'] = ""
            self['cardNum'] = ""
            self['courtName']= ""
            self['areaName'] = ""
            self['partyTypeName'] = ""
            self['gistId'] = ""
            self['regDate'] = ""
            self['gistUnit'] = ""
            self['duty'] = ""
            self['performance'] = ""
            self['disruptTypeName'] = ""
            self['publishDate'] = ""
            self['detailLink'] = ""
        else:
            Item.__init__(self,item)

