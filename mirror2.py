""" mirror.py




    mirrors a website




    Usage: python mirror.py www.site.com




    Author: Joshua A. Campbell




"""




from HTMLParser import HTMLParser




from htmlentitydefs import name2codepoint




import os




import re




import sys




import urllib2







class PageParser(HTMLParser):




    """ class to parse an html page




        html: parsed html ready to save to file




        urls: urls to use for recursive search




    """




    def __init__(self, *args, **kwargs):




        HTMLParser.__init__(self)




        self.html = ""




        self.urls = []




    def handle_starttag(self, tag, attrs):




        self.html += "<" + tag + " "




        for attr in attrs:




            #format urls for recursion




            if attr[0] == 'href':




                #relative to root




                if attr[1].startswith(".."):




                    self.urls.append(attr[1][3:])




                #outbound links




                elif attr[1].startswith("http://"):




                    None




                #links going deeper




                elif attr[1].startswith("/"):




                    self.urls.append("{fp}" + attr[1])




                #same directory as current link




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




                #relative to root




                if attr[1].startswith(".."):




                    self.urls.append(attr[1][3:])




                #outbound links




                elif attr[1].startswith("http://"):




                    None




                #links going deeper




                elif attr[1].startswith("/"):




                    self.urls.append("{fp}" + attr[1])




                #same directory as current link




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




    """ represents the page of a url




        url: url (relative to the page it was found on)




        fp: filepath(what should precede url to make a valid link)




        siteRoot: site root (http://www.example.com)




    """




    def __init__(self, url, fp):




        self.url = url




        self.fp = fp




        self.fileRoot = "site"




        self.siteRoot = "http://" + sys.argv[1]









def save(self):




        url = self.url









        #add and update fpif necessary




        url = re.sub("{fp}", self.fp, url)




        last = url.rfind("/")




        self.fp = url[:last]









        #prep filepath




        filepath = url.split("/")









        #final url




        url = self.siteRoot+"/" + url









        #case for the index page




        if len(filepath) ==1 and not filepath[0]:




            filepath.append("index.html")




        filename = filepath[-1]




 
 
  

        #write to file



        f = open(filepath, 'w')



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
