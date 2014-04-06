#!/usr/bin/env python

from bs4 import BeautifulSoup, Comment
import urllib2

class Shrinkr:

    def __init__(self):
        self.garbageTags = ['script', 'style', 'noscript', 'form', 'input']
        self.containers = []

    def read(self, url):
        usock = urllib2.urlopen(url)
        html = usock.read()
        usock.close()
        self.soup = BeautifulSoup(html)
        self.clean()

    def clean(self):
        comments = self.soup.find_all(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        for tag in self.garbageTags:
            for element in self.soup.find_all(tag):
                element.decompose()
        self.fixRelativeUrls()

    def extractArcicle(self):
        for tag in self.soup.find_all():
            if tag.name == 'p':
                # is a paragraph, let's do some sheeite
                print tag
            else:
                # it's not a paragraph, but it might be...
                return None

    def fixRelativeUrls(self):
        return 'lol'

    def printOut(self):
        print(self.soup.prettify())

    def printText(self):
        print(self.soup.get_text())

s = Shrinkr()
s.read('http://www.bbc.co.uk/news/uk-politics-26843996')
s.extractArcicle()