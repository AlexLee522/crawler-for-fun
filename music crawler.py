version='Version 3.0'
import re
import os
import urllib.request
import urllib.parse
import tkinter
import tkinter.messagebox
from urllib.error import HTTPError
from urllib.error import URLError
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
import requests

session=requests.Session()

class kgmusic():
    def __init__(self,url):
        self.url=url

    def kgmusic_name(self,contentbin):
        kgmusic_name=(self).filename(contentbin)[0:int(len(kgmusic(self).filename(contentbin))-4)]
        return kgmusic_name

    def get_contentbin(self):
            url=self.url.get()
            if len(url)==0:
                tkinter.messagebox.showerror('ERROR','Please enter the URL')
            if url[0:4]!='http':
                url='http://'+url
            pattern='[=].*[&]'
            hash=re.search(pattern,url).group()
            hash=hash[1:len(hash)-1]
            jsonsite='http://www.kugou.com/yy/index.php?r=play/getdata&hash='+hash
            contentbin=urllib.request.urlopen(jsonsite).read()
            return contentbin,url

    def get_content(self,contentbin):
            content=contentbin.decode('utf8') #二进制转utf8 str
            return content

    def filename(self,contentbin):
        albumname=re.search('"audio_name":".*?"', kgmusic(url).get_content(contentbin)).group()
        albumname=albumname[14:len(albumname)-1]
        albumname=albumname.encode('utf-8').decode('unicode_escape')+'.mp3'  #utf8转unicode输出中文
        return albumname

    def get_status(self,test_url): #输出HTTP状态码
        download_status.set("Checking URL validity......  Please wait....")
        gui.update()
        try:
            urllib.request.urlopen(test_url).getcode
        except (HTTPError, ConnectionResetError, URLError, ConnectionRefusedError, ConnectionError, ConnectionAbortedError) :
            download_status.set('Connection Error')
            tkinter.messagebox.showerror('CONNECTION ERROR','Please check your Internet connection')
        else:
            download_status.set("")

    def musicsite(self):
        global pattern2
        global content
        musicsite=re.search(pattern2,content).group()
        musicsite=musicsite[12:len(musicsite)]
        musicsite=musicsite.replace("\\","")
        return musicsite

    def HTTPHeader(self): #添加请求头
        req=urllib.request.Request(self.url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')

    def fileoperation(self,data):
        global contentbin
        path=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+kgmusic(url).filename(contentbin)
        file=open(path,'wb')
        file.write(data)
        file.close()

    def printdling(self,k):
        if k=='0':
            download_status.set('')
        else:
    #        download_status.set("Downloading "+filename(contentbin)[0:int(len(filename(contentbin))-4)]+'...')
            download_status.set("Downloading "+ kgmusic(url).kgmusic_name(contentbin)+"...Please wait")
    def printdled(self,contentbin):
        ed=kgmusic(self).kgmusic_name(contentbin) +' was successfully downloaded!'
        filepath=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'
        text=tkinter.messagebox.showinfo('Tips',ed+'\n\nPlease click the [Open download folder] button to manage files')

    def get_url(self):
        return kgmusic(self).get_contentbin()[1]

    def download(self):
        global url
        global pattern2
        global content
        global contentbin
        contentbin=kgmusic(url).get_contentbin()[0]
        kgmusic(url).printdling('1')
        gui.update()
        content=kgmusic(url).get_content(contentbin)
        pattern2=('"play_url":".*?mp3')  #正则匹配下载链
        data=urllib.request.urlopen(kgmusic(url).musicsite()).read()
        return data,url

    def help_btn(self):
        global filepath
        tkinter.messagebox.showinfo('Help','【QQ音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如https://y.qq.com/n/yqq/song/002s34bV1k1W7M.html）\n3-粘贴到输入框\n4-单击"Download"按钮'+'\n\n\n' + \
                                    '【虾米音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如http://www.xiami.com/song/1802514667）\n3-粘贴到输入框\n4-单击"Download"按钮'+'\n\n\n' + \
                                    '【酷狗音乐】爬取方法：\n'+'1-在酷狗播放器界面播放需要下载的歌\n2-复制网页地址\n（如http://www.kugou.com/song/#hash=1D2B511BB8E33C72AB25466E90FBD020&album_id=0）\n3-粘贴到输入框\n4-单击"Download"按钮'+'\n\n\n'+ \
                                    '请点击[Open download folder]打开下载目录：'+os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'\n\n\n'+version)

    def open_file(self):
        os.startfile (os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

    def main(self):
        global url
        global pattern2
        global content
        global contentbin
        global download_status
        global num
        kgmusic(url).fileoperation(kgmusic(url).download()[0])
        kgmusic(url).printdling('0')
        gui.update()
        kgmusic(url).printdled(contentbin)
        url.set('')
        num=0
        gui.update()


class qqmusic():
    def music_name(self,content):
        music_name = str(BeautifulSoup(content.text, 'html.parser').title)[7:-45]
        return music_name

    def download(self,url):
        global num
        global qqmusic_name
        # 获取输入url中的songmid
        originURL=url.get()
        songmid = originURL[28:-5]
        originURL_content=session.get(url=originURL)
        qqmusic_name=qqmusic().music_name(originURL_content)
        qqmusic().printdling('1',qqmusic_name)
        gui.update()

        # 获取vkey
        vkey_URL = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&songmid=' + \
            songmid + '&filename=C400' + songmid + '.m4a&guid=6113762648'
        data = requests.get(vkey_URL).text.split(',')
        vkey = data[7][8:-5]

        # 获取qq音乐下载url
        download_URL = 'http://dl.stream.qqmusic.qq.com/C400' + songmid + \
            '.m4a?' + vkey + '&guid=6113762648&uin=0&fromtag=66'

        # 下载音乐
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Host': 'dl.stream.qqmusic.qq.com'}
        parameters = {'vkey': vkey}
        data = requests.get(download_URL, headers=headers, params=parameters).content
        file = open(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+qqmusic_name+'.mp3', 'wb')
        num=0
        file.write(data)
        file.close()

    def printdling(self,k,music_name):
        if k=='0':
            download_status.set('')
        else:
            download_status.set("Downloading "+music_name+"......Please wait")

    def printdled(self,qqmusic_name):
        ed=qqmusic_name+' was successfully downloaded!'
        filepath=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'
        text=tkinter.messagebox.showinfo('Tips',ed+'\n\nPlease click the [Open download folder] button to manage files')

    def main(self):
        global qqmusic_name
        global music_name
        global url
        qqmusic().download(url)
        gui.update()
        qqmusic().printdling('0',qqmusic_name)
        qqmusic().printdled(qqmusic_name)
        url.set('')
        gui.update()

class xiami():
    def __init__(self,url):
        self.url=url.get()

    def dl_url(self,s):
        xiami(url).printdling('1')
        gui.update()
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
        xiami_dl_url=urllib.parse.unquote(output).replace('^', '0')
        return xiami_dl_url

    def get_songid(self):
        headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        html = requests.get(url.get(), headers=headers).text
        idpattern = "<link rel=\"canonical\" href=.*? />"
        idresult = re.findall(idpattern, html, re.S)[0]
        songid = str(idresult.split(' ')[2][32:-1])
        return songid

    def music_name(self,url):
        headers={    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        url=url.get()
        xiami_resp=session.get(url=url,headers=headers)
        music_name=str(BeautifulSoup(xiami_resp.text, 'html.parser').head.title).split(',')[0][7::]
        return music_name

    def get_code(self):
        global location
        xiami_originURL = 'http://www.xiami.com/song/playlist/id/' + xiami(url).get_songid() + \
        '/object_name/default/object_id/0/cat/json?_ksTS=1522759378983_389&callback=jsonp390'
        para = {'_ksTS': '1522758305970_389', 'callback': 'jsonp390'}
        referer = 'http://www.xiami.com/play?ids=/song/playlist/id/' + \
            xiami(url).get_songid() + '1/object_name/default/object_id/0'
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Referer': referer}
        location_data = requests.get(xiami_originURL, headers=headers1, params=para).text
        location_list = str(location_data).split(',')
        for i in location_list:
            if 'location' in i:
                num = location_list.index(i)
        location = location_list[num][12:-1]

    def download(self,location):
        global url
        dl_url=xiami(url).dl_url(location)
        song_data=requests.get(dl_url).content
        file=open(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+xiami(url).music_name(url)+'.mp3', 'wb')
        file.write(song_data)
        file.close()

    def printdling(self,k):
        if k=='0':
            download_status.set('')
        else:
            download_status.set("Downloading "+xiami(url).music_name(url)+"....Please wait")

    def printdled(self):
        global music_name
        ed=xiami(url).music_name(url)+' was successfully downloaded!'
        filepath=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'
        text=tkinter.messagebox.showinfo('Tips',ed+'\n\nPlease click the [Open download folder] button to manage files')

    def main(self):
        global url
        xiami(url).get_code()
        xiami(url).download(location)
        gui.update()
        xiami(url).printdling('0')
        xiami(url).printdled()
        url.set('')
        gui.update()

def button():
    global url
    try:
        download_status.set("Checking URL validity......  Please wait....")
        gui.update()
        session.get(url.get())
    except MissingSchema:
        tkinter.messagebox.showerror('ERROR','Please enter an valid URL')
        url.set('')
        download_status.set("")
        gui.update()
        return
    gui.update()
    if 'kugou' in url.get():
        kgmusic(url).main()
    elif 'qq' in url.get():
        qqmusic().main()
    else:
        xiami(url).main()

num=0

if os.path.exists(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music') == False:
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

gui=tkinter.Tk()
download_status = tkinter.StringVar()
download_status.set('')
tkinter.Label(gui,textvariable=download_status).place(x=40,y=60)
gui.update()
gui.title('Music crawler')
gui.geometry('400x200')
tkinter.Label(gui,text='Music URL:').place(x=40,y=30)
url=tkinter.StringVar()
url_area=tkinter.Entry(gui,textvariable=url).place(x=120,y=30)
gui.update()
btn_download=tkinter.Button(gui,text='Download',command=lambda:button(),width=12,height=3).place(x=130,y=80)
gui.update()
btn_path=tkinter.Button(gui,text='Open download folder',command=lambda:kgmusic(url).open_file(),width=18,height=1).place(x=255,y=26)
btn_help=tkinter.Button(gui,text='Help',command=lambda:kgmusic(url).help_btn(),width=4,height=1).place(x=10,y=165)
gui.update()
kgmusic(url).get_status('http://www.baidu.com')
if num == 0:
    num += 1
    tkinter.messagebox.showinfo('Tips','本软件仅供学习交流使用，请勿转载')
gui.mainloop()
