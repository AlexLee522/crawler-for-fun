version='Version 3.3'
import re
import os
import requests
import urllib.request
import urllib.parse
import tkinter
import tkinter.messagebox
import base64
import win32con
import win32clipboard as wcb
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from urllib.error import HTTPError
from urllib.error import URLError
from requests.exceptions import MissingSchema

session=requests.Session()

class kgmusic():
    def __init__(self,url):
        self.url=url

    def kgmusic_name(self,contentbin):
        kgmusic_name=(self).filename(contentbin)[0:int(len(kgmusic(self).filename(contentbin))-4)]
        return kgmusic_name

    def get_contentbin(self):
            url=self.url
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
            download_status.set("Downloading "+ kgmusic(self).kgmusic_name(contentbin))

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
        originURL=url[0:47]
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
            download_status.set("Downloading "+music_name)

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
        url=('')
        gui.update()

class xiami():
    def __init__(self,url):
        self.url=url

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
        html = requests.get(url, headers=headers).text
        idpattern = "<link rel=\"canonical\" href=.*? />"
        idresult = re.findall(idpattern, html, re.S)[0]
        songid = str(idresult.split(' ')[2][32:-1])
        return songid

    def music_name(self,url):
        headers={    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
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
            download_status.set("Downloading "+xiami(url).music_name(url))

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


class Netease():
    def __init__(self,url):
        self.url=url


    def AES_encrypt(self,text, key, iv):
        pad = 16 - len(text) % 16
        if isinstance(text, str):
            text = text + pad * chr(pad)
        else:
            text = text.decode('utf-8') + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text


    def get_params(self,first_param,fourth_param):
        iv = "0102030405060708"  # AES加密的偏移量可以通过抓包获得
        first_key = fourth_param
        second_key = 16 * 'F'  # 16位随机字符
        h_encText = Netease(url).AES_encrypt(first_param, first_key, iv)
        h_encText = Netease(url).AES_encrypt(h_encText, second_key, iv)  # 一共经过两次加密获得encText
        return h_encText


    def get_encSecKey(self):
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey


    # 获取所需的json文件
    def get_json(self,url, params, encSecKey):
        headers = {
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }  # 在请求头中需加入Cookie和Referer
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        response = session.post(self.url, headers=headers, data=data).json()
        return response['data']


    def get_songid(self,song_url):
        headers = {
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }  # 在请求头中需加入Cookie和Referer
        url = song_url[0:20]+song_url[22::]
        data = requests.get(url,headers=headers).text
        pattern = "\"@id\": \".*?\""
        song_id = re.findall(pattern,data)[0].split("/")[3][8:-1]
        return song_id

    
    # 获取歌曲名字
    def get_songname(self,song_id):
        headers = {
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }  # 在请求头中需加入Cookie和Referer

        url = 'http://music.163.com/song?id=' + song_id
        netease_resp = session.get(url, headers=headers)
        song_name=str(BeautifulSoup(netease_resp.text, 'html.parser').title).split('-')[0][7::]+str(BeautifulSoup(netease_resp.text, 'html.parser').title).split('-')[1][0:-1]
        song_name=song_name.replace('  ','-')
        return song_name

    def printdling(self,k,song_id):
        if k=='0':
            download_status.set('')
        else:
            download_status.set("Downloading "+Netease(url).get_songname(song_id))

    def printdled(self,song_id):
        ed=Netease(url).get_songname(song_id)+' was successfully downloaded!'
        filepath=os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'
        text=tkinter.messagebox.showinfo('Tips',ed+'\n\nPlease click the [Open download folder] button to manage files')

        
    def main(self):
        global url
        second_param = "010001"
        third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        fourth_param = "0CoJUm6Qyw8W8jud"
        song_url = self.url
        song_id = Netease(url).get_songid(song_url)
        Netease(url).printdling('1',song_id)
        gui.update()
        first_param = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}" % int(song_id)
        song_name = Netease(url).get_songname(song_id)

        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        params = Netease(url).get_params(first_param,fourth_param)
        encSecKey = Netease(url).get_encSecKey()
        """
        获取的json文件如下
        rsp:{
            'data': [{
                'gain': 2.3073,
                'type': 'mp3',
                'url': 'http://m10.music.126.net/20180111133509/24c79548414f7aa7407985818cb16a39/ymusic/333c/66b1/e5ec/
                    72aeb13aca24c989295e58e8384e3f97.mp3',
                'md5': '72aeb13aca24c989295e58e8384e3f97',
                'flag': 0, 'code': 200, 'payed': 0, 'id': 151619, 'expi': 1200, 'size': 3868307,
                'uf': None, 'br': 128000, 'fee': 0, 'canExtend': False}], 'code': 200}
        """
        rsp = Netease(url).get_json(url, params, encSecKey)
        music_url = rsp[0].get('url')  # 获取下载的mp3的url

        # 写入文件

        music = session.get(music_url)
        file = open(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'/'+Netease(url).get_songname(song_id)+'.mp3', 'wb')
        file.write(music.content)
        Netease(url).printdling('0',song_id)
        Netease(url).printdled(song_id)
        gui.update()

        
class gui_output():
    def read_clipboard(self):
        wcb.OpenClipboard()
        copied_url=wcb.GetClipboardData(win32con.CF_TEXT)
        wcb.CloseClipboard()
        return(copied_url).decode('utf8')

    def help_btn(self):
        global filepath
        tkinter.messagebox.showinfo('Help','【QQ音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如https://y.qq.com/n/yqq/song/002s34bV1k1W7M.html）\n3-单击"Paste & Download"按钮'+'\n\n\n' + \
                                    '【虾米音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如http://www.xiami.com/song/1802514667）\n3-单击"Paste & Download"按钮'+'\n\n\n'\
                                    '【酷狗音乐】爬取方法：\n'+'1-在酷狗播放器界面播放需要下载的歌\n2-复制网页地址\n（如http://www.kugou.com/song/#hash=1D2B511BB8E33C72AB25466E90FBD020&album_id=0）\n3-单击"Paste & Download"按钮'+'\n\n\n'+ \
                                    '【网易云音乐】爬取方法：\n'+'1-前往需要下载的音乐详情页\n2-复制网页地址\n（如http://music.163.com/#/song?id=548785552）\n3-单击"Paste & Download"按钮'+'\n\n\n'+ \
                                    '请点击[Open download folder]打开下载目录：'+os.path.dirname(os.path.realpath(__file__))+'\Downloaded music'+'\n\n\n'+version)


    def open_file(self):
        os.startfile (os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

    def get_status(self,test_url): #输出HTTP状态码
        download_status.set("Checking network connection......Please wait....")
        gui.update()
        try:
            urllib.request.urlopen(test_url).getcode
        except (HTTPError, ConnectionResetError, URLError, ConnectionRefusedError, ConnectionError, ConnectionAbortedError) :
            download_status.set('                      Connection Error')
            tkinter.messagebox.showerror('CONNECTION ERROR','Please check your Internet connection')
        else:
            download_status.set("")

def button():
    global url
    url=gui_output().read_clipboard()
    try:
        download_status.set("Checking URL validity......Please wait....")
        gui.update()
        session.get(url)
    except MissingSchema:
        tkinter.messagebox.showerror('ERROR','Please paste an valid URL')
        download_status.set("")
        gui.update()
        return
    gui.update()
    if 'kugou' in url:
        kgmusic(url).main()
    elif 'qq' in url:
        qqmusic().main()
    elif '163' in url:
        Netease(url).main()
    else:
        try:
            xiami(url).main()
        except IndexError:
            download_status.set("     Xiami's crawler is temporarily failed! Please try again later")

num=0

if os.path.exists(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music') == False:
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+'\Downloaded music')

gui=tkinter.Tk()
download_status = tkinter.StringVar()
download_status.set('')
tkinter.Label(gui,textvariable=download_status).place(x=10,y=180)
gui.update()
gui.title('Music crawler')
gui.geometry('250x240')
url=''
#tkinter.Label(gui,text='Music URL:').place(x=40,y=30)
#url_area=tkinter.Entry(gui,textvariable=url).place(x=120,y=30)
gui.update()
btn_download=tkinter.Button(gui,text='Paste & Download',command=lambda:button(),width=18,height=3).place(x=60,y=15)
gui.update()
btn_path=tkinter.Button(gui,text='Open download folder',command=lambda:gui_output().open_file(),width=17,height=2).place(x=63,y=80)
btn_help=tkinter.Button(gui,text='Help',command=lambda:gui_output().help_btn(),width=5,height=1).place(x=105,y=130)
gui.update()
gui_output().get_status('https://www.baidu.com')
gui.update()
if num == 0:
    num += 1
    tkinter.messagebox.showinfo('Tips','本软件仅供学习交流使用，请勿转载')

gui.mainloop()
