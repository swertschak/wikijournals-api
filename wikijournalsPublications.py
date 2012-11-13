# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import catlib
import wikipedia
import random
import uuid

# Utility routines
def initPublicationList(mysite, logger):
    """
    Create temporary list of all Publications including url (uuid) and title
    """
    publicationList=catlib.Category(mysite,"Publikation")
    initPublicationList={}
    for j in publicationList.articles():
        mypage=wikipedia.Page(mysite,j.title())
        t=mypage.get()
        test=t.split("=")
        tempString=test[1].split("\n")
        initPublicationList.update({j.title():tempString[0]})
    return initPublicationList


def publicationURL():
    """
    Create Publication URL from uuid function
    """
    publicationURL=str(uuid.uuid4())
    return publicationURL

def attributeList():
    """
    Defines the list of publication attributes
    """
    attributeList=["PublicationTitle","Publisher","ReleaseStatus"]
    return attributeList

def checkIfPublicationExist(title,logger,publicationList):
    """
    Checks if given publication exists
    """
    check=[False,"0"]

    for j in publicationList.items():
        if j[1]==title:
            check=[True,j[0]]
            logger.info(j[0])

    if check[0]:
        logger.warning("Publication "+title+" always exist")
    else:
        logger.warning("Publication "+title+" don´t exist")

    return check

# Routines for content creation
def createPublication(content, mysite, logger, publicationList):
    """
    Create new Publication in wikijournals
    """
    check=checkIfPublicationExist(content["PublicationTitle"],logger,publicationList)

    if not check[0]:
        newPublication="{{Publication\n"
        for key in attributeList():
            if key in content:
                newPublication+="|"+key+"="+content[key]+"\n"
        newPublication+="}}"

        comment="New publication added"

        newPublicationUrl=publicationURL()

        mypage=wikipedia.Page(mysite,newPublicationUrl)

        mypage.put(newPublication,comment)
        logger.info("Publication "+content["PublicationTitle"]+" with URL"+newPublicationUrl+" added")

# Routines for content deletion
def removePublication(title,mysite,logger):
    """
    Remove given publication
    """
    mypage=wikipedia.Page(mysite,title)
    mypage.delete(reason="Deleting by bot",prompt="False",)
    logger.info("Publication "+title+" was deleted")

# Routines for content update
def updatePublication(content, mysite, logger, publicationList):
    """
    Update existing Publication in wikijournals
    """

    check=checkIfPublicationExist(content["PublicationTitle"],logger, publicationList)

    if check[0]:
        newPublication="{{Publication\n"
        for key in attributeList():
            if key in content:
                newPublication+="|"+key+"="+content[key]+"\n"
        newPublication+="}}"

        comment="Publication updated"

        mypage=wikipedia.Page(mysite,check[1])
        mypage.put(newPublication,comment)
        logger.info("Publication "+content["PublicationTitle"]+" with URL "+check[1]+" updated")

# Routines for content reading / querying

#def listAllPublication(mysite,publicationList):
#    """
#    Create a list of all publications in wikijournals
#    """
#    articleCategory=catlib.Category(mysite,"Publikation")
#    return articleCategory.articlesList()

def readAttributes(title, mysite, logger,publicationList):
    """
    Return the value of an attribute for a given page
    """
    readAttribute={}

    for key in publicationList.iterkeys():
        if publicationList[key]==title:
            mypage=wikipedia.Page(mysite,key)
            t=mypage.get()
            if t.find("PublicationTitle="+title)>-1:
                articleText=mypage.get()
                articleText=articleText.replace("{{Publication\n","")
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
    testPublication.update({"PublicationTitle":"Nordkurier"})
    testPublication.update({"Publisher":"Kurierverlags GmbH & Co. KG"})
    testPublication.update({"ReleaseStatus":u"Freigegeben"})
    return testPublication

def testCreatePublication(mysite,logger, publicationList):
    """
    Test creating a single publication
    """
    logger.info("Start test - Create publication -")
    testContent=testPublication()
    createPublication(testContent,mysite,logger,publicationList)
    logger.info("End test - Create publication -")

def testUpdatePublication(mysite,logger,publicationList):
    """
    Test updating a single publication
    """
    logger.info("Start test - Update publication -")
    testContent=testPublication()
    updatePublication(testContent,mysite,logger,publicationList)
    logger.info("End test - Update publication -")

def testRemovePublication(mysite,logger,publicationList):
    """
    Test removing a random single publication
    """
    logger.info("Start test - Remove publication -")
    count=0
    randomPublication=random.randint(0,len(publicationList)-1)
    logger.info(randomPublication)
    for key in publicationList.iterkeys():
        count+=1
        if count==randomPublication:
            logger.info(publicationList[key])
            logger.info(key)
            removePublication(key,mysite,logger)
            logger.info("End test - Remove publication -")
            break

def testListAllPublications(mysite, logger,publicationList):
    """
    Test reading all publications
    """
    logger.info("Start test - List all publications -")
    for publication in publicationList.iterkeys():
        logger.info(publication+":"+publicationList[publication])
    logger.info("End test - List all publications -")

def testReadSingleRandomPublication(mysite,logger,publicationList):
    """
    Test reading a single random publication, including content
    """
    logger.info("Start test - Read single random publication -")
    randomPublication=random.randint(1,len(publicationList))
    count=0
    for key in publicationList.iterkeys():
        count+=1
        if count==randomPublication:
            mypage=wikipedia.Page(mysite,key)
            logger.info(publicationList[key])
            publicationText=mypage.get()
            logger.info(publicationText)
            logger.info("End test - Read single random publication -")
            break

def testReadAttribute(mysite,logger,publicationList):
    """
    Test reading value for an random attribute for a random publication
    """

    logger.info("Start test - Read attributes -")

    #publicationList=listAllPublication(mysite)
    randomPublication=random.randint(1,len(publicationList))
    logger.info(randomPublication)
    count=0
    for key in publicationList.iterkeys():
        count+=1
        if count==randomPublication:
            publicationTitle=publicationList[key]
            logger.info(publicationTitle)
            tempAttributeList=attributeList()
            randomAttribute=random.randint(0,len(tempAttributeList)-1)
            logger.info(randomAttribute)
            attribute=tempAttributeList[randomAttribute]
            logger.info(attribute)
            attributes=readAttributes(publicationTitle,mysite,logger,publicationList)
            if attribute in attributes:
                logger.info(attributes[attribute])

    logger.info("End test - Read attributes -")

