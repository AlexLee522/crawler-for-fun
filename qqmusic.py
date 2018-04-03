version='Version 2.0'
import re
import os
import urllib.request
import tkinter
import tkinter.messagebox
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests

session=requests.Session()

class kgmusic():
    def __init__(self,url):
        self.url=url

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

    def get_status(self): #输出HTTP状态码
        try:
            res=urllib.request.urlopen(self.url).getcode
        except HTTPError:
            text=tkinter.messagebox.showerror('ERROR','Please check your Internet connection')

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
        path=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+kgmusic(url).filename(contentbin)
        file=open(path,'wb')
        file.write(data)
        file.close()

    def printdling(self,k):
        if k=='0':
            download_status.set('')
        else:
    #        download_status.set("Downloading "+filename(contentbin)[0:int(len(filename(contentbin))-4)]+'...')
            download_status.set("Downloading ... Please wait")
    def printdled(self,contentbin):
        ed=kgmusic(self).filename(contentbin)[0:int(len(kgmusic(self).filename(contentbin))-4)] +' was successfully downloaded!'
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
        content=kgmusic(url).get_content(contentbin)
        pattern2=('"play_url":".*?mp3')  #正则匹配下载链
        data=urllib.request.urlopen(kgmusic(url).musicsite()).read()
        return data,url

    def help_btn(self):
        global filepath
        tkinter.messagebox.showinfo('Help','【酷狗音乐】爬取方法：\n'+'1-在酷狗播放器界面播放需要下载的歌\n2-复制网页地址\n（如http://www.kugou.com/song/#hash=1D2B511BB8E33C72AB25466E90FBD020&album_id=0）\n3-粘贴到输入框\n4-单击"Download"按钮'+'\n\n\n'+ \
                                    '【QQ音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如https://y.qq.com/n/yqq/song/002s34bV1k1W7M.html）\n3-粘贴到输入框\n4-单击"Download"按钮'+'\n\n\n' + \
                                    '请点击[Open download folder]打开下载目录：'+os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'\n\n\n'+version+'\n本软件仅供学习交流使用，严禁用于商业用途')

    def open_file(self):
        os.startfile (os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

    def main(self):
        global url
        global pattern2
        global content
        global contentbin
        global download_status
        global num
        kgmusic(url).printdling('1')
        gui.update()
        kgmusic(url).fileoperation(kgmusic(url).download()[0])
        kgmusic(url).printdling('0')
        gui.update()
        kgmusic(url).printdled(contentbin)
        url.set('')
        num=0
        gui.update()


class qqmusic():
    def download(self,url):
        global num
        global music_name
        # 获取输入url中的songmid
        originURL=url.get()
        songmid = originURL[28:-5]
        originURL_content=session.get(url=originURL)
        music_name = str(BeautifulSoup(originURL_content.text, 'html.parser').title)[7:-45]
        #music_name= music_name.find(name="keywords")

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
        file = open(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+music_name+'.mp3', 'wb')
        num=0
        file.write(data)
        file.close()

    def printdling(self,k):
        if k=='0':
            download_status.set('')
        else:
            download_status.set("Downloading ... Please wait")

    def printdled(self):
        global music_name
        ed=music_name+' was successfully downloaded!'
        filepath=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'
        text=tkinter.messagebox.showinfo('Tips',ed+'\n\nPlease click the [Open download folder] button to manage files')

    def main(self):
        global url
        qqmusic().printdling('1')
        gui.update()
        qqmusic().download(url)
        gui.update()
        qqmusic().printdling('0')
        qqmusic().printdled()
        url.set('')
        gui.update()

def button():
    global anum
    global url
    gui.update()
    if 'kugou' in url.get():
        kgmusic(url).main()
    else:
        qqmusic().main()

num=0
anum=0
if os.path.exists(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music') == False:
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

gui=tkinter.Tk()
download_status = tkinter.StringVar()
download_status.set('')
tkinter.Label(gui,textvariable=download_status).place(x=40,y=60)
gui.update()
gui.title('Music crawler')
gui.geometry('400x200')
#get_status('https://www.baidu.com')
tkinter.Label(gui,text='Music URL:').place(x=40,y=30)
url=tkinter.StringVar()
url_area=tkinter.Entry(gui,textvariable=url).place(x=120,y=30)
gui.update()
btn_download=tkinter.Button(gui,text='Download',command=lambda:button(),width=12,height=3).place(x=130,y=80)
btn_path=tkinter.Button(gui,text='Open download folder',command=lambda:kgmusic(url).open_file(),width=18,height=1).place(x=255,y=26)
btn_help=tkinter.Button(gui,text='Help',command=lambda:kgmusic(url).help_btn(),width=4,height=1).place(x=10,y=165)
gui.mainloop()
