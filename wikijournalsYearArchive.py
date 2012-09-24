# -*- coding: utf8 -*-
__author__ = 'kruemel'

import os
import os.path
import wikijournalsArticles
import wikipedia
import codecs
import time

### Linux Magazin (from 2011)###

def listHTMLArticles(htmlDir,logger):
    lmMonths=["01","02","03","04","05","06","07","08","09","10","11","12"]

    count=0
    htmlArticles={}
    for i in lmMonths:
        tempHtmlDir=htmlDir+"\\"+i
        for t in os.walk(tempHtmlDir):
            #check if files exist
            if t[2]:
                for j in t[2]:
                    k=os.path.splitext(j)
                    if k[1]==".html":
                        if k[0]<>"index":
                            articleIssue="%d" % int(i)
                            htmlArticles.update({t[0]+"\\"+j:articleIssue})
                        count+=1
    logger.info(str(count)+" html files found")

    return htmlArticles

def readHtmlAttribute(htmlstring,attribute):
    """
    Returns the value of a html attribute, it means the text between html tags
    """
    start=htmlstring.find("<"+attribute)
    start=start+len(attribute)+2
    end=htmlstring.find("</"+attribute)
    value=htmlstring[start:end]
    return value

def readArticlePageFromUrl2011(url):
    """
    Return Article Page reading from the URL
    """
    tempString=os.path.basename(url)
    articlePage=tempString[0:3]
    #articlePage=tempString.split("-")[0]
    articlePage="%d" % int(articlePage)
    return articlePage

def indexLinuxMagazinArticles2011(htmlDir,year,logger):
    """
    Return mandatory index data for articles from html files for the Linux Magazin from 2011
    """
    indexArticles={}
    count=0

    myArticles=listHTMLArticles(htmlDir,logger)

    for i in myArticles.keys():
        indexArticle={}
        myHtmlFile=codecs.open(i,encoding="utf8")
        logger.info("Open "+i)


        myLines=myHtmlFile.readlines()
        articleType="article"
        for j in myLines:
            myLine=j.strip()
            if myLine.find("<h1>News</h1>")>-1:
                articleType="news"
            if myLine.find("<h1>Zacks Kernel-News</h1>")>-1:
                articleType="news"
            if myLine.find("<h1>Zahlen &amp; Trends</h1>")>-1:
                articleType="news"
            if myLine.find("<h1>Leserbriefe</h1>")>-1:
                articleType="news"

        for j in myLines:
            if j.find("<h1>")>-1:
                 if articleType=="article":
                    indexArticle.update({"ArticleTitle":readHtmlAttribute(j,"h1")})
                    indexArticle.update({"JournalTitle":"Linux Magazin"})
                    indexArticle.update({"ArticleYear":year})
                    indexArticle.update({"Page":readArticlePageFromUrl2011(i)})
                    indexArticle.update({"ArticleIssue":myArticles.get(i)})
                    indexArticle.update({"ArticleRubric":"-"})
                    indexArticle.update({"ArticleAuthor":"-"})
                    localDate=time.localtime()
                    localYear=str(localDate[0])
                    localMonth="%0.2d" % localDate[1]
                    localDay="%0.2d" % localDate[2]
                    EntryDate=localYear+"/"+localMonth+"/"+localDay
                    indexArticle.update({"EntryDate":EntryDate})
                    indexArticle.update({"ArticleKeywords":"-"})
                    count+=1
        myHtmlFile.close()
        if indexArticle:
            indexArticles.update({count:indexArticle})


    logger.info(str(count)+" articles")
    return indexArticles

def importLinuxMagazin2011(family,language,htmlDir,year,logger):
    """
    Import Indexdata from Linux Magazin to Wiki
    """

    linuxArticles=indexLinuxMagazinArticles2011(htmlDir,year,logger)
    mysite=wikipedia.getSite(language,family)

    count=0

    for i in linuxArticles.values():
        count+=1
        logger.info("Import article "+str(count)+"/"+str(len(linuxArticles)))
        wikijournalsArticles.createArticle(i,mysite,logger)


def importYearArchive(publication,dataDir,family, language, year, logger):
    """
    Main routine for importing year archives from CD/DVD
    """
    if publication=="Linux Magazin":
        if int(year)>=2011:
            importLinuxMagazin2011(family,language,dataDir,year,logger)




