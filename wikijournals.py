# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import wikipedia
import sys
import logging
import wikijournalsArticles
import wikijournalsPublications
import wikijournalsPublishers
#import wikijournalsDNB
import wikijournalsIVW
import wikijournalsYearArchive
from optparse import OptionParser

def testArticles(family, language, logger):
    # init mysite
    mysite=wikipedia.getSite(language,family)

    # test creation
    wikijournalsArticles.testCreateArticle(mysite,logger)

    # test update
    wikijournalsArticles.testUpdateArticle(mysite,logger)

    # test reading
    # list all
    wikijournalsArticles.testListAllArticles(mysite,logger)

    # list random page
    wikijournalsArticles.testReadSingleRandomArticle(mysite, logger)

    # read attributes
    wikijournalsArticles.testReadAttribute(mysite,logger)

    # test removing
    wikijournalsArticles.testRemoveArticle(mysite,logger)

def testPublications(family, language, logger):
    # init mysite
    mysite=wikipedia.getSite(language,family)

    # test creation
    wikijournalsPublications.testCreatePublication(mysite,logger)

    # test update
    wikijournalsPublications.testUpdatePublication(mysite,logger)

    # test reading
    # list all
    wikijournalsPublications.testListAllPublications(mysite,logger)

    # list random page
    wikijournalsPublications.testReadSingleRandomPublication(mysite, logger)

    # read attributes
    wikijournalsPublications.testReadAttribute(mysite,logger)

    # test removing
    wikijournalsPublications.testRemovePublication(mysite,logger)

def testPublishers(family, language, logger):
    # init mysite
    mysite=wikipedia.getSite(language,family)

    # test creation
    wikijournalsPublishers.testCreatePublisher(mysite,logger)

    # test update
    wikijournalsPublishers.testUpdatePublisher(mysite,logger)

    # test reading
    # list all
    wikijournalsPublishers.testListAllPublishers(mysite,logger)

    # list random page
    wikijournalsPublishers.testReadSingleRandomPublisher(mysite, logger)

    # read attributes
    wikijournalsPublishers.testReadAttribute(mysite,logger)

    # test removing
    wikijournalsPublishers.testRemovePublisher(mysite,logger)

def checkCorrectNumbersOfOptions(args,Count):
    """
    Check the correct count of given commandline options
    """
    Check=True

    if len(args)<Count:
        Check=False

    if not Check:
        logger.info("Wrong number of options")
    return Check

# Setup Logging
logFile="c:\\projekte\\wikijournals\\logs\\wikijournals.log"

handler = logging.StreamHandler(sys.stdout)
frm = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s",
                              "%d.%m.%Y %H:%M:%S")
handler.setFormatter(frm)

handler2=logging.FileHandler(logFile)
handler2.setFormatter(frm)

logger = logging.getLogger()
logger.addHandler(handler)
logger.addHandler(handler2)
logger.setLevel(logging.DEBUG)
logger.info("Start")

# Global Inits
#family="wikijournals_jiffybox"
#mysite=wikipedia.getSite("de",family)

# Setup Commandline Parameters

parser = OptionParser("wikijournals.py [optionen] Operand1 Operand2 Operand3")
parser.add_option("-o", "--operation", dest="operation", help="testArticles, testPublications, testPublishers, importIVWData, indexLinuxMagazinArticles, importLinuxMagazin")

(options, args)=parser.parse_args()

functions = {
    "testArticles" : lambda a,b,c: testArticles(a,b,logger),
    "testPublications" : lambda a,b,c: testPublications(a,b,logger),
    "testPublishers" : lambda a,b,c: testPublishers(a,b,logger),
    "importIVWData" :lambda a,b,c: wikijournalsIVW.importIVWData(a,b,logger),
    "importYearArchive":lambda a,b,c,d,e,f:wikijournalsYearArchive.importYearArchive(a,b,c,d,e,logger),
    None : lambda a, b: a + b
}

# Main program
op = options.operation

if op in functions:
    if op=="testArticles":
        if checkCorrectNumbersOfOptions(args,2):
            functions[op](args[0], args[1], logger)
    elif op=="testPublications":
        if checkCorrectNumbersOfOptions(args,2):
            functions[op](args[0], args[1], logger)
    elif op=="testPublishers":
        if checkCorrectNumbersOfOptions(args,2):
            functions[op](args[0], args[1], logger)
    elif op=="importIVWData":
        if checkCorrectNumbersOfOptions(args,2):
            functions[op](args[0], args[1])
    elif op=="indexLinuxMagazinArticles":
        if checkCorrectNumbersOfOptions(args,2):
            functions[op](args[0], args[1],logger)
    elif op=="importYearArchive":
        if checkCorrectNumbersOfOptions(args,5):
            functions[op](args[0], args[1],args[2],args[3],args[4],logger)
if not op:
    logger.info("No operations were be specified. Enter wikijournals.py -help for more infos")

logger.info("End")
#testArticles()

# test dnb services
#wikijournalsDNB.checkISSNinDNB("1610-6520")
#logger.info("End")


# test ivw import
#csvfile="data\\ivw\\ivwlist.csv"
#wikijournalsIVW.importIVWData(csvfile,mysite,logger)


  