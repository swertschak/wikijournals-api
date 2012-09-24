# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import catlib
import wikipedia
import random

# Utility routines
def articleURL(content):
    """
    Create Article URL from given parameters (ArticleYear, ArticleIssue ,Page ,ArticleTitle)
    """
    urlList=["ArticleYear","ArticleIssue","ArticlePage","ArticleTitle"]
    articleURL=content["JournalTitle"]

    for key in urlList:
        articleURL+="/"+content[key]
    return articleURL

def attributeList():
    """
    Defines the list of article attributes
    """
    attributeList=["ArticleTitle","ArticleSubtitle","JournalTitle","ArticleYear","ArticleIssue"]
    attributeList.extend(["ArticlePage","ArticleRubric","ArticleSubRubric","ArticleAuthor"])
    attributeList.extend(["ArticleWebsite","EntryDate","ArticleKeywords"])
    return attributeList

# Check routines
def checkArticleContent(content, mysite, logger):
    """
    Checks if all mandatory fields are given
    """
    check=True
    if "ArticleTitle" not in content:
        check=False
        logger.warning("ArticleTitle don´t exist")
    if "JournalTitle" not in content:
        check=False
        logger.warning("JournalTitle don´t exist")
    if "ArticleYear" not in content:
        check=False
        logger.warning("ArticleYear don´t exist")
    if "ArticleIssue" not in content:
        check=False
        logger.warning("ArticleIssue dont´t exist")
    if "ArticlePage" not in content:
        check=False
        logger.warning("ArticlePage don´t exist")

    if check:
        mypage=wikipedia.Page(mysite,articleURL(content))
        if mypage.exists():
            check=False
            logger.warning("Article "+"\""+articleURL(content)+"\""+" always exist")

    return check

def checkIfArticleExist(title,mysite,logger):
    """
    Checks if given article exists
    """
    check=False
    mypage=wikipedia.Page(mysite,title)
    if mypage.exists():
        check=True
    else:
        logger.warning("Article "+title+" don´t exist")
    return check

# Routines for content creation
def createArticle(content, mysite, logger):
    """
    Create new Article in wikijournals
    """
    if checkArticleContent(content, mysite, logger):
        newArticle="{{Article\n"
        for key in attributeList():
            if key in content:
                newArticle+="|"+key+"="+content[key]+"\n"
        newArticle+="}}"

        comment="New article added"

        mypage=wikipedia.Page(mysite,articleURL(content))
        mypage.put(newArticle,comment)
        logger.info("Article "+"\""+articleURL(content)+"\""+" added")

# Routines for content deletion
def removeArticle(title,mysite,logger):
    """
    Remove given article
    """
    if checkIfArticleExist(title,mysite,logger):
        mypage=wikipedia.Page(mysite,title)

        if mypage.delete(reason="Deleting by bot",prompt="False"):
            logger.info("Article "+"\""+title+"\""+" was deleted")

# Routines for content update
def updateArticle(content, mysite, logger):
    """
    Update existing Article in wikijournals
    """
    if checkIfArticleExist(articleURL(content),mysite,logger):
        newArticle="{{Article\n"
        for key in attributeList():
            if key in content:
                newArticle+="|"+key+"="+content[key]+"\n"
        newArticle+="}}"

        comment="Article updated"

        mypage=wikipedia.Page(mysite,articleURL(content))

        # Check if content of updating article is the same like the existing article
        oldArticle=mypage.get()
        if oldArticle==newArticle:
            logger.info("No update, content is the same.")
        else:
            mypage.put(newArticle,comment)
            logger.info("Article "+"\""+articleURL(content)+"\""+" updated")

# Routines for content reading / querying

def listAllArticles(mysite):
    """
    Create a list of all articles in wikijournals
    """
    articleCategory=catlib.Category(mysite,"Artikel")
    return articleCategory.articlesList()

def readAttributes(title, mysite):
    """
    Return the value of an attribute for a given page
    """
    readAttribute={}
    mypage=wikipedia.Page(mysite,title)
    if mypage.exists():
        articleText=mypage.get()
        articleText=articleText.replace("{{Article\n","")
        endAttributes=articleText.find("\n}}")
        articleText=articleText[0:endAttributes]
        tempList=articleText.split("\n")
        for i in tempList:
            record=i.replace("|","")
            record=record.split("=")
            readAttribute.update({record[0]:record[1]})
    return readAttribute

# Routines for tests
def testArticle():
    testArticle={}
    testArticle.update({"ArticleTitle":"Volkswagen: Ex-Aufsichtsrat Christian Wulff drohen hohe Schadenersatzforderungen"})
    testArticle.update({"ArticleSubtitle":"Was wusste Wulff"})
    testArticle.update({"JournalTitle":"Wirtschaftswoche"})
    testArticle.update({"ArticleYear":"2012"})
    testArticle.update({"ArticleIssue":"1"})
    testArticle.update({"ArticlePage":"8"})
    testArticle.update({"ArticlePages":"1"})
    testArticle.update({"ArticleRubric":"Menschen der Wirtschaft und der Medien"})
    testArticle.update({"ArticleSubRubric":"Volkswagen"})
    testArticle.update({"ArticleAuthor":"Martin Seiwert"})
    #testArticle.update({"ArticleWebsite":"http://www.heise.de/ct/inhalt/2011/19/26"})
    testArticle.update({"EntryDate":"2012/1/9"})
    testArticle.update({"ArticleKeywords":"VW, Porsche, Wulff"})
    return testArticle

def testCreateArticle(mysite,logger):
    """
    Test creating a single article
    """
    logger.info("Start test - Create article -")
    testContent=testArticle()
    createArticle(testContent,mysite,logger)
    logger.info("End test - Create article -")

def testUpdateArticle(mysite,logger):
    """
    Test updating a single article
    """
    logger.info("Start test - Update article -")
    testContent=testArticle()
    updateArticle(testContent,mysite,logger)
    logger.info("End test - Update article -")

def testRemoveArticle(mysite,logger):
    """
    Test removing a random single article
    """
    logger.info("Start test - Remove article -")
    articleList=listAllArticles(mysite)
    randomArticle=random.randint(1,len(articleList))
    logger.info(articleList[randomArticle].title())
    removeArticle(articleList[randomArticle].title(),mysite,logger)
    logger.info("End test - Remove article -")

def testListAllArticles(mysite, logger):
    """
    Test reading all articles
    """
    logger.info("Start test - List all articles -")
    for article in listAllArticles(mysite):
        logger.info(article)
    logger.info("End test - List all articles -")

def testReadSingleRandomArticle(mysite, logger):
    """
    Test reading a single random article, including content
    """
    logger.info("Start test - Read single random article -")
    articleList=listAllArticles(mysite)
    randomArticle=random.randint(1,len(articleList))
    articleText=articleList[randomArticle].get()
    logger.info(articleText)
    logger.info("End test - Read single random article -")

def testReadAttribute(mysite,logger):
    """
    Test reading value for an random attribute for a random article
    """

    logger.info("Start test - Read attributes -")

    articleList=listAllArticles(mysite)
    randomArticle=random.randint(1,len(articleList))
    articleTitle=articleList[randomArticle].title()
    logger.info(articleTitle)

    tempAttributeList=attributeList()
    randomAttribute=random.randint(1,len(tempAttributeList))
    logger.info(randomAttribute)
    attribute=tempAttributeList[randomAttribute]
    logger.info(attribute)

    attributes=readAttributes(articleTitle,mysite)
    if attribute in attributes:
        logger.info(attributes[attribute])

    logger.info("End test - Read attributes -")








