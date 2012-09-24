# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import catlib
import wikipedia
import random

# Utility routines
def publisherURL(content):
    """
    Create Publisher URL from given parameters (Publisher)
    """
    publisherURL=content["Publisher"]
    return publisherURL

def attributeList():
    """
    Defines the list of publisher attributes
    """
    attributeList=["Publisher","PublisherZipcode","PublisherLocation","PublisherStreet","PublisherWebsite"]
    return attributeList

def checkIfPublisherExist(title,mysite,logger):
    """
    Checks if given publisher exists
    """
    check=False
    mypage=wikipedia.Page(mysite,title)
    logger.info(title)
    if mypage.exists():
        check=True
    else:
        logger.warning("Publisher "+" don´t exist")
    return check

# Routines for content creation
def createPublisher(content, mysite, logger):
    """
    Create new publisher in wikijournals
    """

    if not checkIfPublisherExist(content["Publisher"], mysite, logger):
        newPublisher="{{Publisher\n"
        for key in attributeList():
            if key in content:
                newPublisher+="|"+key+"="+content[key]+"\n"
        newPublisher+="}}"

        comment="New publisher added"

        mypage=wikipedia.Page(mysite,publisherURL(content))
        mypage.put(newPublisher,comment)
        logger.info("Publisher "+publisherURL(content)+" added")

# Routines for content deletion
def removePublisher(title,mysite,logger):
    """
    Remove given article
    """
    if checkIfPublisherExist(title,mysite,logger):
        mypage=wikipedia.Page(mysite,title)
        mypage.delete(reason="Deleting by bot",prompt="False",)
        logger.info("Publisher "+title+" was deleted")

# Routines for content update
def updatePublisher(content, mysite, logger):
    """
    Update existing Publisher in wikijournals
    """

    if checkIfPublisherExist(publisherURL(content),mysite,logger):
        newPublisher="{{Publisher\n"
        for key in attributeList():
            if key in content:
                newPublisher+="|"+key+"="+content[key]+"\n"
        newPublisher+="}}"

        comment="Publisher updated"

        mypage=wikipedia.Page(mysite,publisherURL(content))
        mypage.put(newPublisher,comment)
        logger.info("Publisher "+publisherURL(content)+" updated")

# Routines for content reading / querying

def listAllPublisher(mysite):
    """
    Create a list of all publishers in wikijournals
    """
    articleCategory=catlib.Category(mysite,"Verlag")
    return articleCategory.articlesList()

def readAttributes(title, mysite):
    """
    Return the value of an attribute for a given page
    """
    readAttribute={}
    mypage=wikipedia.Page(mysite,title)
    if mypage.exists():
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
    testPublication.update({"PublisherStreet":u"Putzbrunner Straße 71"})
    testPublication.update({"PublisherWebsite":"http://www.linuxnewmedia.de/"})
    return testPublication

def testCreatePublisher(mysite,logger):
    """
    Test creating a single publisher
    """
    logger.info("Start test - Create publisher -")
    testContent=testPublisher()
    createPublisher(testContent,mysite,logger)
    logger.info("End test - Create publisher -")

def testUpdatePublisher(mysite,logger):
    """
    Test updating a single publisher
    """
    logger.info("Start test - Update publisher -")
    testContent=testPublisher()
    updatePublisher(testContent,mysite,logger)
    logger.info("End test - Update publisher -")

def testRemovePublisher(mysite,logger):
    """
    Test removing a random single publisher
    """
    logger.info("Start test - Remove publisher -")
    publisherList=listAllPublisher(mysite)
    randomPublisher=random.randint(1,len(publisherList))
    logger.info(publisherList[randomPublisher].title())
    removePublisher(publisherList[randomPublisher].title(),mysite,logger)
    logger.info("End test - Remove publisher -")

def testListAllPublishers(mysite, logger):
    """
    Test reading all publishers
    """
    logger.info("Start test - List all publishers -")
    for publisher in listAllPublisher(mysite):
        logger.info(publisher)
    logger.info("End test - List all publisher -")

def testReadSingleRandomPublisher(mysite, logger):
    """
    Test reading a single random publisher, including content
    """
    logger.info("Start test - Read single random publisher -")
    publisherList=listAllPublisher(mysite)
    randomPublisher=random.randint(1,len(publisherList))
    publisherText=publisherList[randomPublisher].get()
    logger.info(publisherText)
    logger.info("End test - Read single random publication -")

def testReadAttribute(mysite,logger):
    """
    Test reading value for an random attribute for a random publisher
    """

    logger.info("Start test - Read attributes -")

    publisherList=listAllPublisher(mysite)
    randomPublisher=random.randint(1,len(publisherList))
    publisherTitle=publisherList[randomPublisher].title()
    logger.info(publisherTitle)

    tempAttributeList=attributeList()
    randomAttribute=random.randint(1,len(tempAttributeList))
    logger.info(randomAttribute)
    attribute=tempAttributeList[randomAttribute]
    logger.info(attribute)

    attributes=readAttributes(publisherTitle,mysite)
    if attribute in attributes:
        logger.info(attributes[attribute])

    logger.info("End test - Read attributes -")




