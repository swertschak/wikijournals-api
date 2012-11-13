# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import catlib
import wikipedia
import random
import uuid

# Utility routines
def initPublisherList(mysite, logger):
    """
    Create temporary list of all Publishers including url (uuid) and title
    """
    publisherList=catlib.Category(mysite,"Verlag")
    initPublisherList={}
    for j in publisherList.articles():
        mypage=wikipedia.Page(mysite,j.title())
        t=mypage.get()
        test=t.split("=")
        tempString=test[1].split("\n")
        initPublisherList.update({j.title():tempString[0]})
    return initPublisherList

def publisherURL():
    """
    Create Publisher URL from given parameters (Publisher)
    """
    publisherURL=str(uuid.uuid4())
    return publisherURL

def attributeList():
    """
    Defines the list of publisher attributes
    """
    attributeList=["Publisher","PublisherHomepage","PublisherLocation","PublisherZipCode","PublisherAdress","ReleaseStatus"]
    return attributeList

def checkIfPublisherExist(title,logger,publisherList):
    """
    Checks if given publisher exists
    """
    check=[False,"0"]

    for j in publisherList.items():
        if j[1]==title:
            check=[True,j[0]]
            logger.info(j[0])

    if check[0]:
        logger.warning("Publisher "+title+" always exist")
    else:
        logger.warning("Publisher "+title+" don´t exist")

    return check

# Routines for content creation
def createPublisher(content, mysite, logger, publisherList):
    """
    Create new publisher
    """
    check=checkIfPublisherExist(content["Publisher"],logger,publisherList)

    if not check[0]:
        newPublisher="{{Publisher\n"
        for key in attributeList():
            if key in content:
                newPublisher+="|"+key+"="+content[key]+"\n"
        newPublisher+="}}"

        comment="New publisher added"

        newPublisherUrl=publisherURL()

        mypage=wikipedia.Page(mysite,newPublisherUrl)

        mypage.put(newPublisher,comment)
        logger.info("Publisher "+content["Publisher"]+" with URL"+newPublisherUrl+" added")

# Routines for content deletion
def removePublisher(title,mysite,logger):
    """
    Remove given publisher
    """
    mypage=wikipedia.Page(mysite,title)
    mypage.delete(reason="Deleting by bot",prompt="False",)
    logger.info("Publisher "+title+" was deleted")

# Routines for content update
def updatePublisher(content, mysite, logger, publisherList):
    """
    Update existing Publisher in wikijournals
    """

    check=checkIfPublisherExist(content["Publisher"],logger, publisherList)

    if check[0]:
        newPublisher="{{Publisher\n"
        for key in attributeList():
            if key in content:
                newPublisher+="|"+key+"="+content[key]+"\n"
        newPublisher+="}}"

        comment="Publisher updated"

        mypage=wikipedia.Page(mysite,check[1])
        mypage.put(newPublisher,comment)
        logger.info("Publisher "+content["Publisher"]+" with URL "+check[1]+" updated")

# Routines for content reading / querying

#def listAllPublisher(mysite):
#    """
#    Create a list of all publishers in wikijournals
#    """
#    articleCategory=catlib.Category(mysite,"Verlag")
#    return articleCategory.articlesList()

def readAttributes(title, mysite, logger,publisherList):
    """
    Return the value of an attribute for a given page
    """
    readAttribute={}

    for key in publisherList.iterkeys():
        if publisherList[key]==title:
            mypage=wikipedia.Page(mysite,key)
            t=mypage.get()
            if t.find("Publisher="+title)>-1:
                articleText=mypage.get()
                articleText=articleText.replace("{{Publisher\n","")
                endAttributes=articleText.find("\n}}")
                articleText=articleText[0:endAttributes]
                tempList=articleText.split("\n")
                for i in tempList:
                    record=i.replace("|","")
                    record=record.split("=")
                    readAttribute.update({record[0]:record[1]})
                return readAttribute


# Routines for tests
def testPublisher():
    testPublication={}
    testPublication.update({"Publisher":"Linux New Media AG"})
    testPublication.update({"PublisherZipcode":"81739"})
    testPublication.update({"PublisherLocation":u"München"})
    testPublication.update({"PublisherAdress":u"Putzbrunner Straße 71"})
    testPublication.update({"PublisherHomepage":"http://www.linuxnewmedia.de/"})
    testPublication.update({"ReleaseStatus":"Freigegeben"})
    return testPublication

def testCreatePublisher(mysite,logger, publisherList):
    """
    Test creating a single publisher
    """
    logger.info("Start test - Create publisher -")
    testContent=testPublisher()
    createPublisher(testContent,mysite,logger,publisherList)
    logger.info("End test - Create publisher -")

def testUpdatePublisher(mysite,logger,publisherList):
    """
    Test updating a single publisher
    """
    logger.info("Start test - Update publisher -")
    testContent=testPublisher()
    updatePublisher(testContent,mysite,logger,publisherList)
    logger.info("End test - Update publisher -")

def testRemovePublisher(mysite,logger,publisherList):
    """
    Test removing a random single publisher
    """
    logger.info("Start test - Remove publisher -")
    count=0
    randomPublisher=random.randint(0,len(publisherList)-1)
    logger.info(randomPublisher)
    for key in publisherList.iterkeys():
        count+=1
        if count==randomPublisher:
            logger.info(publisherList[key])
            logger.info(key)
            removePublisher(key,mysite,logger)
            logger.info("End test - Remove publisher -")
            break

def testListAllPublishers(mysite, logger,publisherList):
    """
    Test reading all publishers
    """
    logger.info("Start test - List all publishers -")
    for publisher in publisherList.iterkeys():
        logger.info(publisher+":"+publisherList[publisher])
    logger.info("End test - List all publications -")

def testReadSingleRandomPublisher(mysite,logger,publisherList):
    """
    Test reading a single random publisher, including content
    """
    logger.info("Start test - Read single random publisher -")
    randomPublisher=random.randint(1,len(publisherList))
    count=0
    for key in publisherList.iterkeys():
        count+=1
        if count==randomPublisher:
            mypage=wikipedia.Page(mysite,key)
            logger.info(publisherList[key])
            publisherText=mypage.get()
            logger.info(publisherText)
            logger.info("End test - Read single random publisher -")
            break

def testReadAttribute(mysite,logger,publisherList):
    """
    Test reading value for an random attribute for a random publisher
    """

    logger.info("Start test - Read attributes -")

    randomPublisher=random.randint(1,len(publisherList))
    logger.info(randomPublisher)
    count=0
    for key in publisherList.iterkeys():
        count+=1
        if count==randomPublisher:
            publisherTitle=publisherList[key]
            logger.info(publisherTitle)
            tempAttributeList=attributeList()
            randomAttribute=random.randint(0,len(tempAttributeList)-1)
            logger.info(randomAttribute)
            attribute=tempAttributeList[randomAttribute]
            logger.info(attribute)
            attributes=readAttributes(publisherTitle,mysite,logger,publisherList)
            if attribute in attributes:
                logger.info(attributes[attribute])

    logger.info("End test - Read attributes -")




