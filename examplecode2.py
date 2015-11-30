import urllib
import os
import re

url = input("URL: ")
jpgget = url.rfind("/")
data = (url[:jpgget+1])
start = int(input("Start Page: "))
type = input("File Type: ")

if not os.path.isdir('jjal'):
	os.mkdir('jjal')
end = False
while(end == False):
	try:
		crawling = urllib.request.urlopen(data+str(start)+type)
		imagefile = crawling.read()
		print("ok")
		f = open("jjal/" + str(start)+type, 'wb')
		f.write(imagefile)
		f.close()
		start += int(1)
	except urllib.error.HTTPError as err:
		if err.code == 404:
			print("null")
			end = True
