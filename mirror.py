from HTMLParser import HTMLParser	  # HTMLParser : html 문서를 분석하는데 필요한 모듈
from htmlentitydefs import name2codepoint # htmlentitydefs : html 문서의 entity들을 정의한 모듈
					  # name2codepoint : htmlentity 이름을 유니코드로 
					  # 매핑하는 모듈
import os     # 운영체제 관련된 모듈로 파일/디렉토리 관련 작업에 필요
import re     # 정규 표현식으로 특정 패턴을 찾고자 할 때 사용
import sys    # 파이썬 인터프리터와 관련된 환경정보 활용
import urllib2 # url(대부분 http 연결)을 open하는데 사용

“”“
PageParser 클래스
html로 작성된 페이지를 분석해서, 링크로 연결된 부분을 재귀적으로 찾아가는 부분. 멤버(html, urls)
html: 파일로 저장할 준비가 된 분석된 html
urls: 반복적 탐색을 위해 사용하는 urls
멤버 : html – 문자열 형식, urls – 리스트
“”“
class PageParser(HTMLParser): 
    def __init__(self, *args, **kwargs):             # 생성자. self - 인스턴스 객체 전달
        HTMLParser.__init__(self)			# 자신을 초기화
        self.html = ""				# html를 “”로 초기화	
        self.urls = []				# urls를 []로 초기화

    def handle_starttag(self, tag, attrs):		# 스타트 테크 핸들 함수
        self.html += "<" + tag + " "		# self.html 에 "<" 와 tag 그리고 " "를 추가해준다
        for attr in attrs:				# attrs의 attr를 초기 값부터 for문으로 돌려서
            if attr[0] == 'href':		# href : hypertext reference의 약자 => 만약 링크 주소이면
                if attr[1].startswith(".."):	# startswith 메소드 : 이 문자열 인스턴스의 시작 부분과 지정한
                                        # 문자열이 일치하는지를 확인함 => attr[1]이 ".."과 일치하면
                    self.urls.append(attr[1][3:])	# self.urls 뒤에다가 attr[1][3:]값을 추가
                elif attr[1].startswith("http://"):     # 그렇지 않고, 만약 attr[1]이 "http://"과 일치하면
                    None			# 아무것도안함

                elif attr[1].startswith("/"):			# 그렇지 않고, 만약 attr[1]이 "/"과 일치하면
                    self.urls.append("{fp}" + attr[1])	# urls에다가 {fp}+attr[1]추가

                else:					# 모두 거짓일 때
                    self.urls.append("{fp}/" + attr[1])	# urls에다가 {fp}/+attr[1]추가

            self.html += attr[0] + "=\"" + attr[1] + "\" " # if문 나와서 self.html 에다가
						        # attr[0]+"=\"" + attr[1] + "\" "를 붙여줌 

        self.html += ">"					# “>”도 붙여줌


    def handle_endtag(self, tag): 		# 엔드 테크 핸들 함수
        self.html += "</" + tag + ">“	# self.html 에다가 ”</“ + tag + ">"를 붙여줌


    def handle_startendtag(self, tag, attrs): # 스타튼테크 핸들 함수
        self.html += "<" + tag + " "	# self.html에다가 “<” tag " "를 붙여줌
        for attr in attrs:		# attrs의 attr가 for문으로 돌 때
            if attr[0] == 'href':		# attr[0] 이 href이면
                if attr[1].startswith(".."):	# attr[1].startswith("..") 이 참이면
                    self.urls.append(attr[1][3:]) # self.urls의 뒤에 attr[1][3:]를 추가해줌

                elif attr[1].startswith("http://"): # attr[1].startswith("http://")이 참이면
                    None		       # 끝

                elif attr[1].startswith("/"):       # attr[1].startswith("/")이 참이면
                    self.urls.append("{fp}" + attr[1]) # self.urls 뒤에 "{fp}"+attr[1]를 추가

                else:
                    self.urls.append("{fp}/" + attr[1]) # self.urls 뒤에 "{fp}/"+attr[1]를 추가

            self.html += attr[0] + "=\"" + attr[1] + "\" "   # self.html에 attr[0] + "=\"" + attr[1] + "\" 							    # "를 계속 추가 한다
        self.html += "/>" 				    # self.html에 "/>"를 계속 추가한다.

    def handle_data(self, data):		# 핸들 데이터 함수
        self.html += data.decode('utf-8')  # self.html에 data.decode('utf-8')를 추가한다.

    def handle_comment(self, data): 		# 커멘트 핸들 함수
        self.html += "<!--" + data + "-->“	# self.html에 "<!--" + data + "-->“를 추가한다.

    def handle_entityref(self, name):	# entityref 핸들
        c = unichr(name2codepoint[name]) # c에 name2codepoint[name]을 받아, 
					   # 유니코드 문자열로 바꾼 것 대입
        self.html += c			   # self.html 에 c를 추가

    def handle_charref(self, name):	# char ref핸들
        if name.startswith('x'):	        # 만약 name이 x로 시작하면

            c = unichr(int(name[1:], 16)) # c는 unichr(int(name[1:], 16)) 이다.

        else:	# 아니면
            c = unichr(int(name))	# c 는 unichr(int(name))이다.

        self.html += c	                # 그 c값을 self.html에 넣어줌.


    def handle_decl(self, data):	        # decl핸들 함수
        self.html += "<!" + data + ">"    # "<!" + data + ">"를 추가해줌!


# Page 클래스
# 페이지를 저장하는 부분. 멤버(url, fp, fileRoot, siteRoot)
# url: 찾은 페이지와 관련된 url
# fp: file 경로(유효한 링크를 만들기 위해 선행되어야하는 url)
class Page(object):	
    """ represents the page of a url			# url의 페이지를 나타냄
        url: url (relative to the page it was found on)	 # 찾은 page를 실체화
        fp: filepath(what should precede url to make a valid link) # 다양한 링크를 만드는 url보다 앞서								   # 가는 것
        siteRoot: site root (http://www.example.com)                 # 사이트루트
    """

    def __init__(self, url, fp):    # 생성자
        self.url = url	      # 클래스의 url은 매개변수 url로 정의
        self.fp = fp	      # 클래스의 fp은 매개변수 fp로 정의
        self.fileRoot = "site"   # 클래스의 fileRoot은 "site"로 초기화
        self.siteRoot = "http:" + sys.argv[1]  # 클래스의 siteRoot는 "http://" + sys.argv[1]로 초기화 => 					     # http:// 사용자가 넘겨준 인자

def save(self):		# 저장	함수
        url = self.url	# 현재의 url를 url에 저장
        #add and update fpif necessary => fpif necessary를 더하고 업데이트해줌
        url = re.sub("{fp}", self.fp, url)  # re : 정규 표현식으로 특정 패턴을 찾고자 할 때 사용. 
                                        # re.sub : 패턴에 일치하는 문자열을 찾아 바꿈. 
                                        # => url에서 {fp}를 self.fp(직접 넣은 값)로 대치한다. 
        last = url.rfind("/")	        # find는 앞에서부터, rfind는 뒤에서부터 검색. 
                                        # 검색 후 "/" 인덱스 반환 => last는 "/"의 인덱스를 저장
        self.fp = url[:last]	        	# url의 처음부터 "/"의 위치(last)까지를 fp에 저장
        filepath = url.split("/")	        # "/"을 기준으로 url을 분리하여 filepath에 저장(리스트가 된다)
        url = self.siteRoot+"/" + url	# url에 self.siteRoot+"/" + 현재 url로 저장
					# => url = "http:// 사용자가 넘겨준 인자" + "/" + url이 된다


        if len(filepath) ==1 and not filepath[0]:	# 만약 filepath의 길이가 1 이고(저장된 항목이 1개), 						# filepath[0]이 없다면
            filepath.append("index.html")        # filepath 리스트의 맨 뒤에 "index.html"을 붙여준다

        filename = filepath[-1]	                # filename 은 filepath의 마지막 값으로 넣어줌

	#create filepath to save on disk 디스크에 저장하기 위해 filepath를 생성한다.
        if not filepath[0]:                       # not(filepath[0])이면
            filepath = os.path.join(self.fileRoot, *filepath[1:-1]) # 자신의 fileRoot("site")에 filepath[1:-1](1
							       # 부터 끝까지)값을 연결
	“”“
	os.path.join(path1[,path2[...]])
	해당 os 형식에 맞도록 입력 받은 경로를 연결함.
	입력 중간에 절대 경로가 나오면 이전에 취합된 경로는 제거하고 다시 연결함
	>>> join('C:\\Python30', 'Script', 'test.py') 
	'C:\\Python30\\Script\\test.py' 
	>>> join('C:\\Python30', 'D:\\Test', 'test.py') 
	'D:\\Test\\test.py'
 	“““

	else: # 그렇지 않다면
	    filepath = os.path.join(self.fileRoot, *filepath[:-1]) # 자신의 fileRoot("site")에 filepath[1:-1](전							      # 체)값을 연결
	        if not os.path.exists(filepath): # filepath의 경로가 존재하지 않으면
	 os.makedirs(filepath)                 # filepath의 경로를 만든다
      
	“”“
	os.path.exists(path)
	입력받은 경로가 존재하면 True를 반환하고, 존재하지 않는 경우는 False를 반환 
	리눅스와 같은 OS에서는 파일이나 디렉터리가 존재하지만 읽기 권한이 없는 경우에도, False를 반환	할 수 있음
	>>> exists('C:\\Python30') 
	True 
	>>> exists('C:\\Python30\\Devanix') 
	False
	“”“

        filepath = os.path.join(filepath, filename) # filepath와 filename 연결
        if os.path.isfile(filepath):                  # filepath가 파일이면
            return                               # 종료 

	“”“
	os.path.isfile(path)
	경로가 파일인지 아닌지 검사합니다. 파일인 경우에는 True를 반환하고, 그 외의 경우 False를 반환. 
	(혹은 해당 경로가 존재하지 않은 경우에는 False를 반환합니다)
	>>> isfile('C:\\Python30\\python.exe') 
	True 
	>>> isfile('C:\\Python26\\python.exe') 
	False
	“”“

 	#write to file			# 파일에 쓰기
        f = open(filepath, 'w')		# 파일포인터 오픈(쓰기모드)
        print "Processing:" , url		# Processing: url 출력
        r = urllib2.urlopen(url)	        # url의 html소스 가져옴(http://hahahia.tistory.com/105 참고)
        if ".html" in filename:	        # 만약 “.html”이 filename 안에 있다면
            parser = PageParser()	# PageParser 객체 생성
            parser.feed( r.read() )	# r(html 소스)를 가져와서 feed 호출
            html = parser.html.encode('ascii', 'replace') # html(PageParser 클래스의 멤버)를 ascii로 인							 # 코딩해서 나타내줌
	
	“”“
	#encode([encoding, [errors]]) : encoding이 있는 바이너리로 변환
	#>>> "가나다".encode('cp949')              #윈도우에서 사용하는 cp949로 변환
	#b'\xb0\xa1\xb3\xaa\xb4\xd9'
	#>>> #"가나다".encode('utf-8')              # utf-8로 변환
	#b'\xea\xb0\x80\xeb\x82\x98\xeb\x8b\xa4'
	#>>> "가나다abc".encode('latin1', 'ignore')  # 에러부분 무시
	#b'abc'
	#>>> "가나다abc".encode('latin1', 'replace') # 에러부분 ?등의 적절한 문자로 대체
	#b'???abc'
	#>>> "가나다abc".encode('latin1', 'xmlcharrefreplace')      # 에러부분 xml표현방식으로 대체
	#b'가나다abc'
	#>>> "가나다abc".encode('latin1', 'backslashreplace')       # 에러부분 역슬래시 표현 방식으로 
								  #변경
	#b'\\uac00\\ub098\\ub2e4abc’
	“”“

            f.write( html )	             # html를 쓴다
            f.close()		             # 파일을 닫는다
            for url in parser.urls:	     # parser.urls에서 url로 for문을 돌릴 때
                nextPage = Page(url, self.fp) # 페이지(url, self.fp)를 다음페이지로 넣음
                nextPage.save()		     # 다음페이지를 저장해준다.
        else:		                     # 만약 “.html”이 filename 안에 없다면
            f.write( r.read() )	             # 파일을 r.read()로 써주고
            f.close()		             # 닫는다.


“”“
메인코드 : 파이썬 소스 이름, 사용자가 전달하려는 인자를 입력하면 Page 클래스에서 객체를 생성하여 save 함수를 호출함		
“”“

if __name__ == '__main__':  # __name__에 __main__이 저장되어 있으면
    if len(sys.argv) == 2:    # sys.argv의 길이가 2이면 
                             # sys.argv : 시스템 인자를 출력. 
			     # print sys.argv[0]는 현재 파이썬 소스의 이름 출력, 
		             # sys.argv[1]부터는 사용자가 넘겨준 인자를 출력
        page = Page("", "")   # Page 클래스 객체 생성 (url = "", fp = ""가 됨)
        page.save()	     # page를 저장

    else:	             # 길이가 2가 아닐 때	

        print "Usage: python" , sys.argv[0], www.example.com # sys.argv의 길이가 2가 아닐 경우
 							      # Usage: python 파이썬 소스 이름
 							      # www.example.com 을 출력

