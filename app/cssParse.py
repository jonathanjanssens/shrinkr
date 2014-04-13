import sys, re, datetime

class cssParser:

    def __init__(self):
        self.cssObject = {}
        self.cssString = ''
        self.removeRules = ['width', 'float', 'position', 'height']
        self.logFile = open('logs/cssParser.log', 'w')
        self.logFile.write('%s: Start\n' % datetime.datetime.utcnow())

    def loadFile(self, fileName):
        with open(fileName, 'r') as file:
            self.css = file.read().replace('\n', '')
        return self

    def minify(self):
        self.css = re.sub(r'\s+', ' ', self.css)
        # remove leading white space
        self.css = re.sub(r"\s+([!{};:>+\(\)\],])", r"\1", self.css)
        # remove trailing white space
        self.css = re.sub(r"([!{}:;>+\(\[,])\s+", r"\1", self.css)
        return self

    def objectify(self):
        # convert string to lowercase to avoid case problems
        self.css = self.css.lower()
        self.css = self.css.split('}')
        temp = []
        for i in self.css:
            i = i.split('{')
            temp.append(i)
        for t in temp[:-1]:
            self.cssObject[t[0]] = dict(item.split(":") for item in t[1][:-1].split(";"))
        return self

    def fix(self):
        for selector, rules in self.cssObject.items():
            for key, value in rules.items():
                if key in self.removeRules:
                    self.logFile.write('%s: Deleted %s { %s:%s } \n' % (datetime.datetime.utcnow(), selector, key, value))
                    del rules[key]
        self.out()
        return self

    def out(self):
        self.logFile.write('')
        self.logFile.write('%s: End\n' % datetime.datetime.utcnow())
        self.logFile.close()

    def getString(self):
        return self.cssString

    def toCssString(self):
        for key, value in self.cssObject.items():
            self.cssString += '%s%s' % (key, value)

cp = cssParser()
cp.loadFile('../tests/test.css').minify().objectify().fix()
cp.toCssString()
print cp.getString()