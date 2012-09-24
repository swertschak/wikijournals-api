# -*- coding: utf-8 -*-
"""
This family file was auto-generated by $Id: generate_family_file.py 9179 2011-04-15 10:59:23Z xqt $
Configuration parameters:
  url = http://46.252.24.52/mediawiki
  name = wikijournals_jiffybox

Please do not commit this to the SVN repository!
"""

import family

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikijournals_jiffybox'
        self.langs = {
            'de': u'wikijournals.de',
        }

        self.namespaces[4] = self.namespaces.get(4, {})
        self.namespaces[4]['de'] = [u'Wikijournals']
        self.namespaces[5] = self.namespaces.get(5, {})
        self.namespaces[5]['de'] = [u'Wikijournals Diskussion']
        self.namespaces[102] = self.namespaces.get(102, {})
        self.namespaces[102]['de'] = [u'Attribut', u'Property']
        self.namespaces[103] = self.namespaces.get(103, {})
        self.namespaces[103]['de'] = [u'Attribut Diskussion', u'Property talk']
        self.namespaces[104] = self.namespaces.get(104, {})
        self.namespaces[104]['de'] = [u'Datentyp', u'Type']
        self.namespaces[105] = self.namespaces.get(105, {})
        self.namespaces[105]['de'] = [u'Datentyp Diskussion', u'Type talk']
        self.namespaces[106] = self.namespaces.get(106, {})
        self.namespaces[106]['de'] = [u'Formular', u'Form']
        self.namespaces[107] = self.namespaces.get(107, {})
        self.namespaces[107]['de'] = [u'Formular Diskussion', u'Form talk']
        self.namespaces[108] = self.namespaces.get(108, {})
        self.namespaces[108]['de'] = [u'Konzept', u'Concept']
        self.namespaces[109] = self.namespaces.get(109, {})
        self.namespaces[109]['de'] = [u'Konzept Diskussion', u'Concept talk']
        self.namespaces[274] = self.namespaces.get(274, {})
        self.namespaces[274]['de'] = [u'Widget']
        self.namespaces[275] = self.namespaces.get(275, {})
        self.namespaces[275]['de'] = [u'Widget talk']
        self.namespaces[420] = self.namespaces.get(420, {})
        self.namespaces[420]['de'] = [u'Layer', u'Ebene']
        self.namespaces[421] = self.namespaces.get(421, {})
        self.namespaces[421]['de'] = [u'Layer talk', u'Ebene Diskussion']


    def scriptpath(self, code):
        return {
            'de': u'',
        }[code]

    def version(self, code):
        return {
            'de': u'1.16.5',
        }[code]