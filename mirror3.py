from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import os
import re
import sys
import urllib2

class PageParser(HTMLParser):

    def __init__(self, *args, **kwargs):

        HTMLParser.__init__(self)
        self.html = ""
        self.urls = []


    def handle_starttag(self, tag, attrs):

        self.html += "<" + tag + " "
        for attr in attrs:

            if attr[0] == 'href':

                if attr[1].startswith(".."):

                    self.urls.append(attr[1][3:])

                elif attr[1].startswith("http://"):

                    None

                elif attr[1].startswith("/"):

                    self.urls.append("{fp}" + attr[1])

                else:

                    self.urls.append("{fp}/" + attr[1])

            self.html += attr[0] + "=\"" + attr[1] + "\" "

        self.html += ">"


    def handle_endtag(self, tag):

        self.html += "</" + tag + ">"


    def handle_startendtag(self, tag, attrs):

        self.html += "<" + tag + " "

        for attr in attrs:

            if attr[0] == 'href':

                if attr[1].startswith(".."):

                    self.urls.append(attr[1][3:])


                elif attr[1].startswith("http://"):

                    None


                elif attr[1].startswith("/"):

                    self.urls.append("{fp}" + attr[1])

                else:

                    self.urls.append("{fp}/" + attr[1])

            self.html += attr[0] + "=\"" + attr[1] + "\" "

        self.html += "/>"



    def handle_data(self, data):

        self.html += data.decode('utf-8')


    def handle_comment(self, data):

        self.html += "<!--" + data + "-->"


    def handle_entityref(self, name):

        c = unichr(name2codepoint[name])
        self.html += c



    def handle_charref(self, name):

        if name.startswith('x'):

            c = unichr(int(name[1:], 16))

        else:

            c = unichr(int(name))

        self.html += c



    def handle_decl(self, data):

        self.html += "<!" + data + ">"




class Page(object):


    def __init__(self, url, fp):

        self.url = url
        self.fp = fp
        self.fileRoot = "site"
        self.siteRoot = "http://" + sys.argv[1]



    def save(self):

        url = self.url
        url = re.sub("{fp}", self.fp, url)
        last = url.rfind("/")
        self.fp = url[:last]
        filepath = url.split("/")
        url = self.siteRoot+"/" + url

        if len(filepath) ==1 and not filepath[0]:

            filepath.append("index.html")

        filename = filepath[-1]
        f = open(filename, 'w')
        print "Processing:" , url
        r = urllib2.urlopen(url)

        if ".html" in filename:

            parser = PageParser()
            parser.feed( r.read() )
            html = parser.html.encode('ascii', 'replace')
            f.write( html )
            f.close()

            for url in parser.urls:

                nextPage = Page(url, self.fp)
                nextPage.save()

        else:
            f.write( r.read() )
            f.close()



if __name__ == '__main__':

    if len(sys.argv) == 2:

        page = Page("", "")
        page.save()

    else:
        print "Usage: python" , sys.argv[0], "www.example.com"
