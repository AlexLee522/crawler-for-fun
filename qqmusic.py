import requests


# 获取输入url中的songmid
url0 = input('输入目标url:')
songmid = url0[28:-5]

# 获取vkey
vkeyurl = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&songmid=' + \
    songmid + '&filename=C400' + songmid + '.m4a&guid=6113762648'
data = requests.get(vkeyurl).text.split(',')
vkey = data[7][8:-5]

songurl = 'http://dl.stream.qqmusic.qq.com/C400' + songmid + \
    '.m4a?' + vkey + '&guid=6113762648&uin=0&fromtag=66'

# 下载音乐
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Host': 'dl.stream.qqmusic.qq.com'}
parameters = {'vkey': vkey}
data = requests.get(songurl, headers=headers, params=parameters).content
file = open('qqmusic1.m4a', 'wb')
file.write(data)
file.close()
