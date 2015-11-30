#--*--coding:utf-8--*--
import re #导入re库，正则表达式库
import urllib.request 
from urllib.error import URLError,HTTPError 
import sys

url = "http://www.hainu.edu.cn/stm/xinxi/shtml_liebiao.asp@bbsid=5419.shtml"
# 给文件加入头信息，用以模拟浏览器访问
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
j=1 #第j张照片，后面用到
for i in range(5419,5426):
    try: #try是一种处理异常的语句
        #实现翻页翻页
        url1 = re.sub('bbsid=\d+','bbsid=%d'%i,url,re.S) #sub实现替换功能
        print(url1)
        #发送请求，获得返回信息
        req1 = urllib.request.Request(url1,headers=headers) #模拟浏览器请求访问url1
        response = urllib.request.urlopen(req1,timeout=15) #返回一个 http.client.HTTPResponse 对象，允许延迟15秒
        content1 = response.read().decode('gbk') #以'gbk'的编码格式读取
        #处理获取的web网页，并将信息处理了
        items1 = re.findall('<a target="_blank" href="(.*?)">',content1,re.S) #进行正则匹配

        for url2 in items1:
            url2 = 'http://www.hainu.edu.cn' + url2
            req2 = urllib.request.Request(url2,headers=headers)
            response = urllib.request.urlopen(req2,timeout=15)
            content2 = response.read().decode('gbk')
            picurl = re.findall('<a target="_blank" title="在新窗口打开" href=(.*?)>',content2,re.S)
            if len(picurl) > 0 :
                picurl0 = 'http://www.hainu.edu.cn' + picurl[0]
                pic = urllib.request.urlopen(picurl0)
                jpgpic = pic.read()
                #首先你得有个pic文件夹
                fp = open('pic/'+str(j)+'.jpg',"wb") #以二进制写
                print('正在捕获第%d位老师'%j)
                # 写入文件
                fp.write(jpgpic)
                fp.close()
                j=j+1
          
    except HTTPError as e: # except为异常类型，e为异常处理代码段
        print("HTTPError")
    except URLError as e:
        print("URLError")
