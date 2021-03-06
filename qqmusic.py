import requests
import re


# 获取输入url中的songmid
url0 = input('输入目标url:')
songmid = url0[28:-5]

# 获取歌曲名称
pattern = "<title>.*?</title>"
namedata = requests.get(url0).text
songname = re.findall(pattern, namedata, re.S)[0].split('&')[0][7::]

# 获取vkey
vkeyUrl = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&songmid=' + \
    songmid + '&filename=C400' + songmid + '.m4a&guid=6113762648'
vkeyData = requests.get(vkeyUrl).text.split(',')
vkey = vkeyData[7][8:-5]

songUrl = 'http://dl.stream.qqmusic.qq.com/C400' + songmid + \
    '.m4a?' + vkey + '&guid=6113762648&uin=0&fromtag=66'

# 下载音乐
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Host': 'dl.stream.qqmusic.qq.com'}
parameters = {'vkey': vkey}
data = requests.get(songUrl, headers=headers, params=parameters).content
file = open('%s.m4a' % songname, 'wb')
file.write(data)
file.close()
