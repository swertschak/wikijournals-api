# -*- coding: utf-8 -*-
__author__ = 'kruemel'

import urllib

def checkISSNinDNB(issn):
    sruServer="http://services.d-nb.de/sru"
    sruCatalog="/dnb"
    sruVersion="?version=1.1"
    sruOperation="&operation=searchRetrieve"
    sruID="dc.identifier%3D"
    sruQuery=sruServer+sruCatalog+sruVersion+sruOperation+"&query="+sruID+issn
    f=urllib.urlopen(sruQuery)
    t=f.readlines()
    fobj = open("dnb.txt", "w")
    for i in t:
        fobj.write(i)
    fobj.close
    return sruQuery

print checkISSNinDNB("1610-6520")