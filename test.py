#-*-coding:utf-8
import urllib
from urllib import urlopen
#html_source = urllib.urlopen('http://www.naver.com').read()
html_source = urllib.urlopen('http://www.koreatech.ac.kr').read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_source)
f = open('moviedasd.txt', 'w')
# 테그 이름을 변수 이름으로 사용할 수 있다.


f.write(str(soup.html.head.title))
# 결과: <title>페이지 제목</title>


# 계층구조의 중간단계를 생략할 수 있다.
f.write(str(soup.title))
# 결과: <title>페이지 제목</title>


# 테그 안에 다른 테그가 없는 경우 string 속성으로 테그 내용을 얻을 수 있다.
#f.write(soup.title.string)
# 결과: 페이지 제목


# 같은 이름의 테그가 여러개 있다면 제일 먼저 나오는 테그를 알려준다.
# dictionary 문법을 사용하여 테그의 속성만 얻을 수도 있다.
f.write(str(soup.p))
# 결과: <p class="layout"><b>첫번째 단락</b></p>
f.write(str(soup.p['class']))
# 결과: layout


# 없는 테그를 지칭하면 (BeautifulSoup.) Null 객체를 반환한다.
f.write(str(soup.body.title))
# 결과: Null


# soup('p') 은 첫번째 뿐아니라 모든 p 테그 목록을 반환한다.
# 두번째 아규먼트로 테그의 속성을 제한할 수도 있다.
f.write(str(soup('p')[0]))
# 결과: <p class="layout"><b>첫번째 단락</b></p>
f.write(str(soup('img', { 'name': 'main', })))
# 결과: [<img src="dooly-1.png" name="main" height="100" width="70" />]
f.write(str(soup('p', 'layout')))
# soup('p', { 'class': 'layout' }) 과 같다. CSS 분류를 쉽게 지정할 수 있다.


# parent 속성은 계층구조상 한칸 위에 있는 테그를 지칭하고, 반대로 contents

# 속성은 계층구조상 한칸 아래에 있는 테그 목록을 반환한다.
# nextSibling 와 previousSibling 은 계층구조상 같은 위치에 있는 바로 앞뒤 테그를

# 지칭한다.  예제에서 첫번째 p 테그의 nextSibling 은 두번째 p 테그가 아니라

# 첫번째 p 테그와 두번째 p 테그 사이 영역이고, 이 영역에는 줄바꿈 문자 하나만 있다.
# 이는 soup('p').parent.contents 로 확인할 수 있다.
# next 와 previous 는 계층구조와 무관하게 HTML 소스에서 테그 바로 앞뒤에 위치하는

# 테그를 지칭한다.  마지막으로 테그 이름은 name 속성에 저장된다.
f.write(str(soup('p')[0].nextSibling))
# 결과: \n
f.write(str(soup('p')[0].next))
# 결과: <b>첫번째 단락</b>

f.write(str(soup('p')[0].next.name))
# 결과: b
# 앞에서 본 string 속성은 테그 안에 다른 테그가 없는 경우에는 contents[0] 과 같고,
# 다른 테그가 있다면 Null 이다.

f.write(str(len(soup('p')))) # len(soup('p').contents) 와 같다.
for x in soup('p'): # for x in soup('p').contents: 와 같다.

    pass

## fetch(name, attrs, recursive, limit) 함수
# 다양한 조건을 가지고 원하는 테그를 찾는 함수로, 앞의 예들은 이 함수의 축약형이다.

#       tag.fetch(...) = tag(...)
# name과 attrs는 각각 테그 이름과 테그 속성을 나타내는데 다양한 방법으로 지시할 수 있다.

#
# * 문자열: fetch('img'), 모든 img 테그 목록
# * 목록: fetch(['object', 'applet', 'embed']), 모든 object/applet/embed 테그 목록
# * dictionary: fetch('div', { 'class': 'sidebar', 'name': 'menu' })
# * 정규표현식: fetch('div', { 'name': re.compile('list.*') }),

#                                           name 속성이 "list"로 시작하는 모든 div 테그 목록
# * 함수: 원하는 조건인 경우 참을 반환하는 함수를 사용하여 복잡한 조건을 지시할 수 있다.

#
# recursive와 limit는 계층구조상 현재 테그 아래를 계속 찾아들어갈지, 만약 그렇다면

# 어느정도까지 들어갈지를 정한다.  기본적으로 현재 테그 아래로 끝까지 들어가면서

# 테그를 찾는다.

#
# fetch() 를 기준삼아 first(), fetchText(), firstText(), findNextSibling(),

# findPreviousSibling(), fetchNextSibling(), fetchPreviousSibling(),
# findNext(), findPrevious(), fetchNext(), fetchPrevious(), findParent(),
# fetchParent() 와 같은 함수가 있다.  fetch*/*Text() 함수는 테그가 아닌 테그 안의

# 문자를 찾거나 가져오고, *Next*/*Previous*/*Parent() 함수는 현재 테그에서

# 계층구조상 아래로 내려가지 않고 대신 앞뒤 혹은 위로 이동하며 조건에 맞는 테그를

# 찾는다.  각 함수의 자세한 정보는 설명서를 참고하라.
def need_thumbnail(x):
    # 가로나 세로가 60 보다 큰 img 테그라면 True, 아니면 False

    if x.name == 'img':

        return x.get('height', 0) > 60 or x.get('width', 0) > 60

    return False
f.write(str(soup.ul(need_thumbnail))) # = soup.ul.fetch(need_thumbnail)
f.write(str(soup.p.findNextSibling('p'))) # 두번째 p 테그

# 다음과 같이 HTML 소스를 수정할 수도 있다.  단, 이때는 앞에서 본 string 같은
# 축약형을 사용할 수 없고 contents 목록을 직접 수정해야 한다.  그후 prettify()

# 함수로 수정한 HTML 소스를 계층구조에 따라 들여쓰기하여 출력한다.
f.write(str(soup))
soup.title.contents[0] = '제목 수정'
soup.p['class'] = 'menu'
soup('p')[1].contents = ['두번째 단락 생략',]

del soup.body.contents[5]
f.write(str(soup.prettify()))
f.close()
