import requests
import re
import urllib.parse


# 解密 location
def getFinalUrl(s):
    rows = int(s[0])
    strlen = len(s) - 1
    cols = strlen // rows
    right_rows = strlen % rows
    new_s = s[1::]
    output = ''
    for i in range(len(new_s)):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
        output += new_s[int(p)]
    return urllib.parse.unquote(output).replace('^', '0')


orgurl = input('请输入url：')

# 获取songid  歌曲名
headers0 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
html = requests.get(orgurl, headers=headers0).text

idpattern = "<link rel=\"canonical\" href=.*? />"
idresult = re.findall(idpattern, html, re.S)[0]
songid = idresult.split(' ')[2][32:-1]

namepattern = "<meta property=\"og:title\" content=.*?/>"
nameresult = re.findall(namepattern, html, re.S)[0]
songname = nameresult.split(' ')[2][9:-3]


# 获取location并解密
url1 = 'http://www.xiami.com/song/playlist/id/' + songid + \
    '/object_name/default/object_id/0/cat/json?_ksTS=1522759378983_389&callback=jsonp390'
para = {'_ksTS': '1522758305970_389', 'callback': 'jsonp390'}
referer = 'http://www.xiami.com/play?ids=/song/playlist/id/' + \
    songid + '1/object_name/default/object_id/0'
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Referer': referer}
lodata = requests.get(url1, headers=headers1, params=para).text
lolist = str(lodata).split(',')
for i in lolist:
    if 'location' in i:
        num = lolist.index(i)
location = lolist[num][12:-1]

# 下载歌曲
finalUrl = getFinalUrl(location)
songdata = requests.get(finalUrl).content
file = open('%s.mp3' % songname, 'wb')
file.write(songdata)
file.close()
