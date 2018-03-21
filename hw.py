import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
from PIL import Image
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getimg():
    url = "https://uniportal.huawei.com/uniportal/jsp/image.jsp"
    data = urllib.request.urlopen(url).read()
    with open("code.jpg", 'wb') as f:
        f.write(data)
    im = Image.open('code.jpg')
    im.show()
    im.close()
    captcha_solution = input("请输入验证码:")
    captcha_solution = int(captcha_solution)
    return captcha_solution


def loginto(code):
    file_name = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(file_name)
    hanlder = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(hanlder)
    user_name = input('user name:')
    password = input('password')
    loginurl = "https://uniportal.huawei.com/uniportal/login.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        'Connection':'keep-alive',
        'Referer':'https://uniportal.huawei.com/uniportal/login.do'}
    data = {'uid': user_name, 'password': password, 'verifyCode':code,'loginFlag':'byUid','getloginMethod':'null','actionFlag':'loginAuthenticate'}
    postdata = urllib.parse.urlencode(data).encode()
    print(postdata)
    req = urllib.request.Request(loginurl, postdata, headers)
    try:
        #tarurl = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000012007&partNo=d001&play=1"        
        #get_request = urllib.request.Request(tarurl, headers=headers)
        response = opener.open(req)
        page = response.read().decode()
        #file = open('bigdata.mp4', 'wb')
        #file.write(get_response)
        #file.close()
    except urllib.error.URLError as e:
        print(e.code,':',e.reason)

    cookie.save(ignore_discard=True,ignore_expires=True)
    try:
        #for i in range(2,10):
        #    get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d00%s&play=1" % str(i)
        #    get_request = urllib.request.Request(get_url,headers=headers)
        #    get_response = opener.open(get_request).read()
        #    file = open('bigdata0%d.mp4' % i, 'wb')
        #    file.write(get_response)
        #    file.close()
        #    print('已爬取第个0%d视频' % i)
        for i in range(ord('a'),ord('h')+1):
            get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d02%s&play=1" % chr(i)
            get_request = urllib.request.Request(get_url,headers=headers)
            get_response = opener.open(get_request).read()
            file = open('bigdata2%s.mp4' % chr(i), 'wb')
            file.write(get_response)
            file.close()
            print('已爬取第个2%s视频' % chr(i))
        for i in range(0,10):
            get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d02%s&play=1" % str(i)
            get_request = urllib.request.Request(get_url,headers=headers)
            get_response = opener.open(get_request).read()
            file = open('bigdata2%d.mp4' % i, 'wb')
            file.write(get_response)
            file.close()
            print('已爬取第个2%d视频' % i)
        #for i in range(ord('a'),ord('z')+1):
        #    get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d01%s&play=1" % chr(i)
        #    get_request = urllib.request.Request(get_url,headers=headers)
        #    get_response = opener.open(get_request).read()
        #    file = open('bigdata1%s.mp4' % chr(i), 'wb')
        #    file.write(get_response)
        #    file.close()
        #    print('已爬取第个1%s视频' % chr(i))
        #for i in range(0,10):
        #    get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d02%s&play=1" % str(i)
        #    get_request = urllib.request.Request(get_url,headers=headers)
        #    get_response = opener.open(get_request).read()
        #    file = open('bigdata2%d.mp4' % i, 'wb')
        #    file.write(get_response)
        #    file.close()
        #    print('已爬取第个2%d视频' % i)
        #for i in range(ord('a'),ord('h')+1):
        #    get_url = "http://download.huawei.com/edownload/enterprise/DSDPVideo!video.action?contentType=TRAIN&contentId=Node1000010885&partNo=d01%s&play=1" % chr(i)
        #    get_request = urllib.request.Request(get_url,headers=headers)
        #    get_response = opener.open(get_request).read()
        #    file = open('bigdata1%s.mp4' % chr(i), 'wb')
        #    file.write(get_response)
        #    file.close()
        #    print('已爬取第个2%s视频' % chr(i))
    except urllib.error.URLError as e:
        print(e.code,':',e.reason)



a = getimg()
loginto(a)
