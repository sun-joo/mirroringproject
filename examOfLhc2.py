import urllib
import re

def testmain():
    videoid = "KIvwdpYII7s"

    url = u"http://www.youtube.com/get_video_info?video_id=%s&el=embedded&ps=default&eurl=" % videoid

    f = urllib.urlopen(url)

    info = urllib.unquote(f.read())

    r = "token=(.*?)&"

    token = re.findall(r, info)

    downloadurl = u"http://www.youtube.com/get_video?video_id=%s&t=%s&eurl=&el=embedded&ps=default" % (videoid, token)

    downloadWebRequest = urllib.urlopen(downloadurl)

    outfile = open("a.flv", "wb")
    outfile.write(downloadWebRequest.read())
    outfile.close()
    
if __name__ == "__main__":
    testmain()
    
