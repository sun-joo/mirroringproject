#-*- coding: utf-8 -*-   
import os
import re
from urllib import urlopen
import urllib
import requests
import sys
import bs4
reload(sys)
sys.setdefaultencoding("utf-8")


#웹 파싱
response = urlopen("http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf")
s=str(unicode(response.read(), "euc-kr").encode("utf-8"))
#구글링해서 찾은 방법 써봐도 한글깨짐 현상이 나타남..
print 'html source'
print s
print
git 
if not os.path.exists('site'):
	os.makedirs('site')

f = open('site/'+'index.html', 'w')
f.write(s)
f.close()


#베스트셀러 순위별로 책 링크 가져오기(느림)
response = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf' )  
soup = bs4.BeautifulSoup(response.text)  
book_page_urls = [a.attrs.get('href') for a in soup.select('div.title a[href^="http://www.kyobobook.co.kr/product/detailViewKor.laf"]')]  
title2=[0]*30
i=1    
    
print 'Bestseller Data'

#책별로 데이터 가져오기  
for book_page_url in book_page_urls:  
    response = requests.get( book_page_url )  
    soup = bs4.BeautifulSoup(response.text)  
        
    title = soup.select( 'h1.title strong' )[0].get_text().strip()  
    author = soup.select( 'span.name  a' )[0].get_text().strip()    
    date = soup.select( 'span.date' )[0].get_text().strip()   
    price=soup.select( 'ul.list_detail_price span.sell_price' )[0].get_text().strip()   
    print title + '/' + author + '/' + date + '/' + price
    print
    title2[i]=title
    i=i+1

#베스트셀러 20위까지 이미지 저장(파일 이름: x위 제목)
fileNo = 1
url = 'http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf'

f = urllib.urlopen(url)
html = f.read()

exp = re.compile(r'<img.+?src="(http://image.kyobobook.co.kr/images/book/large/[0-9]+/\w+.jpg)".*?>')
imageUrlList=exp.findall(html)

if not os.path.exists('kyobo'):
    os.makedirs('kyobo')

for url in imageUrlList:
    print 'Save File:', fileNo
    contents = urllib.urlopen(url).read()
    if(fileNo<10):
    	f=open("kyobo/"+'0'+str(fileNo)+'위 '+title2[fileNo]+'.jpg', 'wb')
    	f.write(contents)
    #file(str(fileNo)+'.jpg', 'wb').write(contents)
    else:
    	f=open("kyobo/"+str(fileNo)+'위 '+title2[fileNo]+'.jpg', 'wb')
    	f.write(contents)
    fileNo = fileNo + 1

