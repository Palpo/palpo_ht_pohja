# -*- coding: utf-8 -*-

import urllib2
from urlparse import urlparse
import re

# pip install lxml
from lxml.html import fromstring


# KEYWORD_SPLITTER.split("Juuri... näin!") --> ["Juuri", "näin"]
KEYWORD_SPLITTER = re.compile('[\W_]+', flags=re.UNICODE)


def imgsFromUrl(url):
    """
    Lataa html-sivun annetusta urlista ja kaivaa siitä kuvat (img-elementit)
    sekä kuviin liittyviä avainsanoja.
    
    Avainsanat ei aina ole kovin järkeviä...
    
    Palauttaa dictionaryn:
        { 'http://www.example.com/pic1.png': ['keyword1', 'keyword2', ...],
          'http://www.example.com/pic2.jpg': ['keyword3', 'keyword4', ...],
           ...
        }
    """
    
    ret = {}
    doc = downloadHtmlDoc(url)
    doc.make_links_absolute(url)
    for img in doc.findall('.//img'):
        src = img.get('src')
        kws = extractKeywords(img)
        if src in ret:
            ret[src] += kws
        else:
            ret[src] = kws
    return ret


def downloadFile(url):
    return makeRequest(url).read()


def downloadHtmlDoc(url):
    res = makeRequest(url)
    encoding = getEncoding(res)
    content = unicode(res.read(), encoding)
    return fromstring(content)  


def makeRequest(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Palpo-agentti"}) 
    return urllib2.urlopen(req)


def getEncoding(res):
    ct = res.headers['content-type']
    if not ct or 'charset=' not in ct:
        return 'utf-8'
    return ct.split('charset=')[-1].strip()


def extractKeywords(imgElement):
    # Avainsanat kaivetaan kuvan tiedostonimestä, img:n alt-attribuutista, parentin tekstisisällöstä
    keywords = set()
    filename = urlparse(imgElement.get('src','')).path.split('/')[-1]
    keywords.update(KEYWORD_SPLITTER.split(filename.rsplit('.',2)[0]))
    keywords.update(KEYWORD_SPLITTER.split(imgElement.get('alt', '')))
    pt = imgElement.getparent().text_content()
    if pt:
        keywords.update(KEYWORD_SPLITTER.split(pt))
    return [kw.lower() for kw in keywords if kw]

