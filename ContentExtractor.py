#!/usr/bin/env python

import argparse

from Evaluate import Evaluate
from Menu import Menu
from bs4 import BeautifulSoup, Comment, NavigableString
from collections import OrderedDict
from urlparse import urlparse
import urllib2
import robotparser

class ContentExtractor:

    def __init__(self, extractorUrl=None):
        self.garbageTags = ['script', 'style', 'noscript', 'form', 'input']
        self.articleContainer = None
        self.containers = {}
        self.url = ''
        self.extractorUrl = extractorUrl
        self.robotparser = robotparser.RobotFileParser()
        self.userAgentString = 'Shrinkr/0.9 (http://shrinkr.jonathanjanssens.com/about.php)'
        self.urlComponents = urlparse(self.url)
        self.head = ''
        self.allLinks = []

    def read(self, url):
        self.url = url
        self.fixUrl()
        self.robotparser.set_url('%s://%s/robots.txt' % (self.urlComponents.scheme, self.urlComponents.netloc))
        self.robotparser.read()
        if self.robotparser.can_fetch(self.userAgentString, self.url) is False:
            raise RuntimeError('Shrinkr is blocked by the robots.txt file for this site.')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', self.userAgentString)]
        html = opener.open(self.url)
        self.soup = BeautifulSoup(html)
        self.clean()

    def fixUrl(self):
        if self.url[:4] != 'http':
            self.url = 'http://%s' % (self.url)
        self.urlComponents = urlparse(self.url)


    def clean(self):
        comments = self.soup.find_all(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        for tag in self.garbageTags:
            for element in self.soup.find_all(tag):
                element.decompose()
        self.head = self.soup.find('head').extract()
        self.allLinks = self.soup.find_all('a', href=True)
        self.fixRelativeUrls()

    def makeMenu(self):
        self.menu = Menu(self.allLinks, self.urlComponents.netloc, extractorUrl=self.extractorUrl)
        self.menu.sortLinks()
        self.menuHTML = self.menu.make()
        with open('tpl/controls.tpl', 'r') as html:
            self.controlsHTML = html.read().replace('{{ orginal_url }}', self.url)

    def extractArticle(self):
        if self.extractorUrl is not None:
            self.extractLinkedArticles()
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
        
        self.articleContainer = self.containers.popitem()[0]

    def getExtractedArticle(self, prependHead=True):
        article = ''
        # append menu and controls to self.articleContainer
        self.articleContainer.insert(1, self.menuHTML)
        self.articleContainer.insert(2, self.controlsHTML)
        # append js and the end and css to self.head
        with open('static/shrinkr.css', 'r') as css:
            self.head.insert(2, '<style>%s</style>' % css.read())
        with open('static/shrinkr.js', 'r') as js:
            self.articleContainer.insert(len(self.articleContainer.contents), '<script>%s</script>' % js.read())
        #
        if prependHead is True:
            article = unicode.join(u'\n',map(unicode,self.head))
        article += unicode.join(u'\n',map(unicode,self.articleContainer))
        return article

    def getExtractedArticleText(self):
        return self.articleContainer.get_text()

    def fixRelativeUrls(self):
        for a in self.soup.find_all('a', href=True):
            if a['href'][:4] != 'http':
                if a['href'][:1] == '#' or a['href'][:1] == '?':
                    a['href'] = '%s://%s%s%s' % (self.urlComponents.scheme, self.urlComponents.netloc, self.urlComponents.path, a['href'])
                else:
                    a['href'] = '%s://%s/%s' % (self.urlComponents.scheme, self.urlComponents.netloc, a['href'])

    def extractLinkedArticles(self):
        for a in self.soup.find_all('a', href=True):
            a['href'] = '%s%s' % (self.extractorUrl, a['href'])

    def debugOutput(self):
        for k, v in self.containers.items():
            print k.name, k.attrs, v

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url for html extraction')
    parser.add_argument('-e', '--extractorUrl', help='define extractor url', type=str, default=False)
    parser.add_argument('-p', '--printHTML', help='print out article HTML after extraction', action='store_true')
    parser.add_argument('-t', '--printText', help='print out article text only after extraction', action='store_true')
    parser.add_argument('-d', '--debug', help='enable debug mode', action='store_true')
    args = parser.parse_args()
    
    s = ContentExtractor(extractorUrl='http://something.loc/?extract=')
    s.read(args.url)
    
    s.makeMenu()
    s.extractArticle()
    
    if args.debug:
        print s.debugOutput()
    
    if args.printHTML:
        print s.getExtractedArticle()
    if args.printText:
        print s.getExtractedArticleText()