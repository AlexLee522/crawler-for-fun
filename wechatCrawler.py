import requests
import re
from urllib.parse import quote
import time

key = input("输入查询关键词：")
keycode = quote(key) #对关键词进行编码
url = "http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&s_from=input&page=1" % keycode #page参数确定页数
pageData = requests.get(url).text #抓取查询结果页面
pagePattern = "<h3>.*?</h3>"
result = re.findall(pagePattern, pageData, re.S) #使用正则爬取包含具体信息的部分
# 创建空的列表 保存title writer posttime 一起保存在information中
title = []
writer = []
posttime = []
information = []
# 使用循环爬取每页的数据 每页默认10页
for i in range(10):
	# 爬取具体内容的url
	urlpattern = "href=\".*?\""
	url0 = re.findall(urlpattern, result[i], re.S)[0]
	url = url0.replace("amp;","")
	
	# 爬取具体数据并写入html文件
	data = requests.get(url[6:-1]).text
	file = open("%d.html" % i,"wb")
	file.write(data)
	file.close()
	
	# 使用正则获取文章标题
	titlePattern = "<title>.*?</title>"
	title.append(re.findall(titlePattern, data, re.S)[0][7:-8])
	
	# 使用正则获取文章发表时间
	posttimePattern = "<em id=\"post-date\" class=\"rich_media_meta rich_media_meta_text\">.*?</em>"
	posttime.append(re.findall(posttimePattern, data, re.S)[0][64:-5])

	# 使用正则获取文章作者
	writerPattern = "<a class=\"rich_media_meta rich_media_meta_link rich_media_meta_nickname\" href=\"##\" id=\"post-user\">.*?</a>"
	writer.append(re.findall(writerPattern, data, re.S)[0][98:-4])
	
	# 将所有信息保存在列表中
	information.append("文章题目：%s" % title[i] +"--"+ "作者：%s" % writer[i] +"--"+ "发表时间：%s" % posttime[i])
	
	time.sleep(1) # 爬取一次 sleep 1秒 防止被封

print(information)
