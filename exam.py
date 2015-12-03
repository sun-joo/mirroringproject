# 2015-12-03 test
import urllib

URL ='http://newsstand.naver.com/?list=ct1&pcode=001' #naver 
urllib.urlretrieve(URL,URL.split('/')[-1])

#success! but video don't download . only img
