import re
import urllib.request
import socket  # 超时设置


class proxy:
    #构建请求头
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)

    def getIpPool():
        tarurl = 'http://www.xicidaili.com'
        data = urllib.request.urlopen(tarurl).read().decode('utf8')

        # 利用正则匹配ip地址和端口
        pattern = '<tr class="">.*?</tr>'
        result0 = re.findall(pattern, data, re.S)

        # 循环爬取整个网页,构建列表
        proxy = []
        for i in range(len(result0)):
            pattern1 = '<td>.*</td>'
            result = re.findall(pattern1, result0[i], re.S)
            resultlist = result[0].split()
            patternip = resultlist[0][4:-5]  # 获取IP地址
            patternport = resultlist[1][4:-5]  # 获取目标端口
            data = '%s:%s' % (patternip, patternport)
            proxy.append(data)
        return proxy

    def useProxy(addlist, url):
            # 使用代理ip获取网页
        for i in addlist:
            proxy = urllib.request.ProxyHandler({'http': i})
            opener = urllib.request.build_opener(
                proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            try:
                status = urllib.request.urlopen(url).getcode()
                if status == 200:
                    timeout = 4
                    socket.setdefaulttimeout(timeout)  # 超时设置
                    data = urllib.request.urlopen(url).read().decode('utf8')
                    if '有道' and '无效用户' not in data:  # 有时候返回有道的网页，很无奈，求解决
                        return data
            except:
                continue


# 举个栗子
tarurl = 'http://www.lysteel.com/'
addlist = proxy.getIpPool()
print(proxy.useProxy(addlist, tarurl))
