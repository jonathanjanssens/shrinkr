#
# TODO:
#   * Fix links going to external origin when they start with www or http
#

from urlparse import urlparse

class Menu:

    def __init__(self, links, baseUrl, extractorUrl=None, templateFile=None):
        self.links = links
        self.baseUrl = baseUrl
        self.internalLinks = []
        self.externalLinks = []
        self.extractorUrl = extractorUrl
        self.menuHTML = ''
        if templateFile is not None:
            self.templateFile = templateFile
        else:
            self.templateFile = 'tpl/menu.tpl'

    def sortLinks(self):
        for a in self.links:
            u = urlparse(a['href'])
            if a.get_text() is '':
                continue
            if u.netloc == self.baseUrl:
                self.internalLinks.append(a)
            else:
                self.externalLinks.append(a)
        if self.extractorUrl is not None:
            for a in self.internalLinks:
                a['href'] = self.extractorUrl + a['href']
            for a in self.externalLinks:
                a['href'] = self.extractorUrl + a['href']

    def make(self):
        internal = ''
        external = ''
        with open(self.templateFile, 'r') as html:
            for a in self.internalLinks:
                temp = "<li><a href='%s'>%s</a></li>" % (a['href'], a.get_text())
                internal += temp
            for a in self.externalLinks:
                temp = "<li><a href='%s'>%s</a></li>" % (a['href'], a.get_text())
                external += temp
            self.menuHTML = html.read().replace('{{ internal_origin_links }}', internal).replace('{{ external_origin_links }}', external)
        if self.extractorUrl is not None:
            with open('tpl/form.tpl', 'r') as form:
                self.menuHTML = self.menuHTML.replace('{{ shrinkr_form }}', form.read().replace('{{ extractor_url }}', self.extractorUrl))
        else:
            self.menuHTML = self.menuHTML.replace('{{ shrinkr_form }}', '')
        return self.menuHTML