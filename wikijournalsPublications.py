# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import catlib
import wikipedia
import random

# Utility routines
def publicationURL(content):
    """
    Create Publication URL from given parameters (JournalTitle)
    """
    publicationURL=content["JournalTitle"]
    return publicationURL

def attributeList():
    """
    Defines the list of publication attributes
    """
    attributeList=["JournalTitle","ISSN","Publisher","JournalWebsite","JournalDNBInfo"]
    return attributeList

def checkIfPublicationExist(title,mysite,logger):
    """
    Checks if given publication exists
    """
    check=False
    mypage=wikipedia.Page(mysite,title)
    logger.info(title)
    if mypage.exists():
        check=True
    else:
        logger.warning("Publication "+" don´t exist")
    return check

# Routines for content creation
def createPublication(content, mysite, logger):
    """
    Create new Article in wikijournals
    """

    if not checkIfPublicationExist(content["JournalTitle"], mysite, logger):
        newPublication="{{Journal\n"
        for key in attributeList():
            if key in content:
                newPublication+="|"+key+"="+content[key]+"\n"
        newPublication+="}}"

        comment="New publication added"

        mypage=wikipedia.Page(mysite,publicationURL(content))
        mypage.put(newPublication,comment)
        logger.info("Publication "+publicationURL(content)+" added")

# Routines for content deletion
def removePublication(title,mysite,logger):
    """
    Remove given article
    """
    if checkIfPublicationExist(title,mysite,logger):
        mypage=wikipedia.Page(mysite,title)
        mypage.delete(reason="Deleting by bot",prompt="False",)
        logger.info("Publication "+title+" was deleted")

# Routines for content update
def updatePublication(content, mysite, logger):
    """
    Update existing Publication in wikijournals
    """

    if checkIfPublicationExist(publicationURL(content),mysite,logger):
        newPublication="{{Journal\n"
        for key in attributeList():
            if key in content:
                newPublication+="|"+key+"="+content[key]+"\n"
        newPublication+="}}"

        comment="Publication updated"

        mypage=wikipedia.Page(mysite,publicationURL(content))
        mypage.put(newPublication,comment)
        logger.info("Publication "+publicationURL(content)+" updated")

# Routines for content reading / querying

def listAllPublication(mysite):
    """
    Create a list of all publications in wikijournals
    """
    articleCategory=catlib.Category(mysite,"Publikation")
    return articleCategory.articlesList()

def readAttributes(title, mysite):
    """
    Return the value of an attribute for a given page
    """
    readAttribute={}
    mypage=wikipedia.Page(mysite,title)
    if mypage.exists():
        articleText=mypage.get()
        articleText=articleText.replace("{{Journal\n","")
        endAttributes=articleText.find("\n}}")
        articleText=articleText[0:endAttributes]
        tempList=articleText.split("\n")
        for i in tempList:
            record=i.replace("|","")
            record=record.split("=")
            readAttribute.update({record[0]:record[1]})
    return readAttribute

# Routines for tests
def testPublication():
    testPublication={}
    testPublication.update({"JournalTitle":"Berliner Morgenpost"})
    testPublication.update({"ISSN":"1433-3511"})
    testPublication.update({"Publisher":"Axel Springer AG"})
    testPublication.update({"JournalWebsite":"http://www.morgenpost.de/"})
    testPublication.update({"JournalDNBInfo":"http://d-nb.info/018318312"})
    return testPublication

def testCreatePublication(mysite,logger):
    """
    Test creating a single publication
    """
    logger.info("Start test - Create publication -")
    testContent=testPublication()
    createPublication(testContent,mysite,logger)
    logger.info("End test - Create publication -")

def testUpdatePublication(mysite,logger):
    """
    Test updating a single publication
    """
    logger.info("Start test - Update publication -")
    testContent=testPublication()
    updatePublication(testContent,mysite,logger)
    logger.info("End test - Update publication -")

def testRemovePublication(mysite,logger):
    """
    Test removing a random single publication
    """
    logger.info("Start test - Remove publication -")
    publicationList=listAllPublication(mysite)
    randomPublication=random.randint(1,len(publicationList))
    logger.info(publicationList[randomPublication].title())
    removePublication(publicationList[randomPublication].title(),mysite,logger)
    logger.info("End test - Remove publication -")

def testListAllPublications(mysite, logger):
    """
    Test reading all publications
    """
    logger.info("Start test - List all publications -")
    for publication in listAllPublication(mysite):
        logger.info(publication)
    logger.info("End test - List all publications -")

def testReadSingleRandomPublication(mysite, logger):
    """
    Test reading a single random publication, including content
    """
    logger.info("Start test - Read single random publication -")
    publicationList=listAllPublication(mysite)

    randomPublication=random.randint(1,len(publicationList))
    publicationText=publicationList[randomPublication].get()
    logger.info(publicationText)
    logger.info("End test - Read single random publication -")

def testReadAttribute(mysite,logger):
    """
    Test reading value for an random attribute for a random publication
    """

    logger.info("Start test - Read attributes -")

    publicationList=listAllPublication(mysite)
    randomPublication=random.randint(1,len(publicationList))
    publicationTitle=publicationList[randomPublication].title()
    logger.info(publicationTitle)

    tempAttributeList=attributeList()
    randomAttribute=random.randint(1,len(tempAttributeList))
    logger.info(randomAttribute)
    attribute=tempAttributeList[randomAttribute]
    logger.info(attribute)

    attributes=readAttributes(publicationTitle,mysite)
    if attribute in attributes:
        logger.info(attributes[attribute])

    logger.info("End test - Read attributes -")

