#!/usr/bin/env python

from Evaluate import Evaluate
from bs4 import BeautifulSoup, Comment, NavigableString
from collections import OrderedDict
import argparse
import urllib2

class Shrinkr:

    def __init__(self):
        self.garbageTags = ['script', 'style', 'noscript', 'form', 'input', 'head']
        self.articleContainer = None
        self.containers = {}
        self.url = ''

    def read(self, url):
        self.url = url
        self.fixUrl()
        usock = urllib2.urlopen(self.url)
        html = usock.read()
        usock.close()
        self.soup = BeautifulSoup(html)
        self.clean()

    def fixUrl(self):
        if self.url[:4] != 'http':
            self.url = 'http://%s' % (self.url)

    def clean(self):
        comments = self.soup.find_all(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        for tag in self.garbageTags:
            for element in self.soup.find_all(tag):
                element.decompose()
        self.fixRelativeUrls()

    def extractArcicle(self):
        # create some class to queue the evaluations or pass the tag like evaluate.asXX(tag)
        for tag in self.soup.find_all()[::-1]:
            evaluate = Evaluate()
            if tag.name == 'p':
                evaluate.asParagraph(tag)
            else:
                for child in tag.children:
                    if isinstance(child, NavigableString):
                        text = unicode(child).strip()
                        if len(text) > 10:
                            evaluate.asParagraph(child)
                            continue
                    else:
                        evaluate.asContainer(child)
                evaluate.asContainer(tag)
                self.containers[tag] = evaluate.score
        self.containers = OrderedDict(sorted(self.containers.items(), key=lambda t: t[1])) # sort based on value (ASC)
        
        print self.containers.popitem()


    def fixRelativeUrls(self):
        return 'lol'

    def printOut(self):
        print(self.soup.prettify())

    def printText(self):
        print(self.soup.get_text())

parser = argparse.ArgumentParser()
parser.add_argument('url', help='url for html extraction')
parser.add_argument('-d', '--debug', help='enable debug mode')
args = parser.parse_args()

s = Shrinkr()
#s.read('http://www.bbc.co.uk/news/uk-politics-26843996')
s.read(args.url)
s.extractArcicle()