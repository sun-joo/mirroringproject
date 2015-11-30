from urllib import urlopen
response = urlopen('http://www.koreatech.ac.kr')
print(response.read().decode('utf-8'))
