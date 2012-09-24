# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import wikijournalsPublications
import codecs

def importIVWData(csvfile, mysite, logger):
    """
    Import Publications from CSV into wikijournals
    """
    localIVWList=[]
    myfile=codecs.open(csvfile,"r",encoding="latin-1")

    # Remove redundant entries
    for line in myfile:
        record=line.split(";")
        JournalTitle=record[1].strip()
        if JournalTitle not in localIVWList:
            localIVWList.append(JournalTitle)
    myfile.close()
    count=0

    # Write publications to wikijournals
    for line in localIVWList:
        count+=1
        #logger.info(str(count)+" von "+str(len(localIVWList))+": "+line)
        content={"JournalTitle":line}
        content.update({"ISSN":"-"})
        content.update({"Publisher":"-"})
        wikijournalsPublications.createPublication(content,mysite,logger)

