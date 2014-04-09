class Evaluate:

    def __init__(self):
        self.tagNameBonuses = {'p': 50, 'div': -100, 'h1': 40, 'h2': 50, 'h3': 40, 'h4': 30}

    def load(self):
        self.textDensity = 0.0
        self.textLength = 0
        self.childTags = 0
        self.score = 0
        self.calculateTextLength()
        self.countChildren()
        self.calculateTextDensity()

    def calculateTextLength(self):
        text = unicode(self.element).strip()
        self.textLength = len(text)
        return self.textLength

    def countChildren(self):
        try:
            self.childTags = len(self.element.findChildren())
        except AttributeError:
            self.childTags = 0
        return self.childTags

    def calculateTextDensity(self):
        try:
            self.textDensity = float(self.textLength) / float(self.childTags)
        except ZeroDivisionError:
            self.textDensity = self.textLength
        return self.textDensity

    def asContainer(self, tag):
        self.element = tag
        self.load()
        for child in self.element.findChildren(recursive=False):
            self.score += child.score
        try:
            if tag.name in self.tagNameBonuses:
                self.score += self.tagNameBonuses[tag.name]
        except AttributeError:
            pass
        tag.score = self.score

    def asParagraph(self, tag):
        self.element = tag
        self.load()
        self.score = self.textDensity
        tag.score = self.textDensity