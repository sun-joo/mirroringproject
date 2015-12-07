#-*-coding: cp949-*- 

import urllib2
page = urllib2.urlopen("http://navercast.naver.com/contents.nhn?rid=68&contents_id=1268&leafId=68")
from bs4 import BeautifulSoup
f = open('bestseller1987.txt','w')

soup = BeautifulSoup(page)
a = soup.findAll('a',attrs={"target":"_blank"})
for i in range(6, 45):
    if (i%2) == 0:    
        bookname = a[i].text.encode("utf-8") 
        print bookname
    elif (i%2) != 0:  
        authorname = a[i].text.encode("utf-8") 
        print authorname
        name = bookname + ',' + authorname 
        f.write(name+'\n')  
f.close()  


#!/usr/bin/env python
 
import httplib
from urlparse import urljoin, urlunparse
from urllib import urlretrieve
from HTMLParser import HTMLParser
import os
 
class ImageParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    if tag != 'img':
      return
    if not hasattr(self, 'result'):
      self.result = []
    for name, value in attrs:
      if name == 'src':
        self.result.append(value)
 
def downloadImage(srcUrl, data):
  if not os.path.exists('DOWNLOAD'):
    os.makedirs('DOWNLOAD')
 
  parser = ImageParser()
  parser.feed(data)
  resultSet = set(x for x in parser.result)
 
  for x in sorted(resultSet):
    src = urljoin(srcUrl,x)
    basename = os.path.basename(src)
    targetFile = os.path.join('DOWNLOAD', basename)
 
    print "Downloading,..,", src
    urlretrieve(src, targetFile)
 
def main():
  host = "http://navercast.naver.com/contents.nhn?rid=68&contents_id=1268&leafId=68"
 
  conn = httplib.HTTPConnection(host)
  conn.request("GET",'')
  resp = conn.getresponse()
 
  charset = resp.msg.getparam('charset')
  data = resp.read().decode(charset)
  conn.close()
 
  print "\n>>>>>> Download Images from ", host
  url = urlunparse(('http',host, '','','',''))
  downloadImage(url,data)
 
if __name__ == '__main__':
  main()

