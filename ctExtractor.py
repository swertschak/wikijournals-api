__author__ = 'kruemel'

import urllib
import logging
from optparse import OptionParser
import sys

def extractArticle(year,issue,page):
    """
    Extract Properties (title, keywords) from articles for a given page
    """

    urlBase="http://www.heise.de/ct/inhalt/"
    urlCommand=urlBase+str(year)+"/"+str(issue)+"/"+str(page)

    filehandle=urllib.urlopen(urlCommand)
    count=0
    foundKeywords=-1
    wikiArticle="{{Article\n"
    articleTitle="|ArticleTitle="
    articleJournal="|JournalTitle=CT\n"

    articleYear="|ArticleYear="+str(year)+"\n"
    articleIssue="|ArticleIssue="+str(issue)+"\n"
    articlePage="|Page="+str(page)+"\n"
    articleKeywords="|ArticleKeywords="

    articleIndex=articleYear+articleIssue+articlePage
    articleWebsite="|ArticleWebsite="+urlCommand+"\n"

    articleRubric="|ArticleRubric="
    articleSubTitle="|ArticleSubtitle="
    
    for i in filehandle:
        i = i.strip()
        count+=1
        if i.find("<h2>")>-1:
            i=i.replace("<h2>","")
            i=i.replace("</h2>","")
            logger.info("Title:"+i)
            articleTitle+=i+"\n"
        if i.find("<h3>")>-1:
            i=i.replace("<h3>","")
            i=i.replace("</h3>","")
            articleSubTitle+=i+"\n"
            logger.info("Subtitle:"+i)
        if i.find('<p class="rubrik_schlagwort">')>-1:
            i=i.replace('<p class="rubrik_schlagwort">',"")
            i=i.replace("</p>","")
            articleRubric+=i+"\n"
            logger.info("Rubric:"+i)
        if i.find("<strong>Schlagw&ouml;rter:</strong>")>-1:
            foundKeywords=count
        if count==foundKeywords+1:
            articleKeywords+=i+"\n"
            logger.info("Keywords:"+i)
    filehandle.close()

    wikiArticle+=articleTitle+articleSubTitle+articleJournal+articleIndex+articleRubric+articleWebsite+"|EntryDate=\n"+articleKeywords
    wikiArticle+= "}}"
    logger.info(wikiArticle)
    return wikiArticle

def checkIfArticleExists(year,issue,page,title):
    """
    Check if an article always exist in the wiki.
    """

    check=False

    urlBase="http://wikijournals.info/index.php5/CT/"
    urlCommand=urlBase+str(year)+"/"+str(issue)+"/"+str(page)+"/"+str(title)

    filehandle=urllib.urlopen(urlCommand)

    for i in filehandle:
        logger.info(i)

    return check

# Setup Logging

handler = logging.StreamHandler(sys.stdout)
frm = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s",
                              "%d.%m.%Y %H:%M:%S")
handler.setFormatter(frm)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Setup Commandline Parameters

parser = OptionParser("ctExtractor.py [optionen] Operand1 Operand2")
parser.add_option("-o", "--operation", dest="operation", help="extractTerms, createPentaXML, normalizeXML")

(optionen, args)=parser.parse_args()


functions = {
       "extractArticle" : lambda a,b,c: extractArticle (a,b,c),
       None : lambda a, b: a + b
       }

# Main program

op = optionen.operation

if op in functions:
    if op=="extractArticle":
        functions[op](args[0], args[1], args[2])

checkIfArticleExists(2013,10,20,"test")


