# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 03:01:08 2018

@author: fuwen

https://www.ximalaya.com/revision/play/album?albumId=12891461&pageNum=1
"""
from lxml import etree
import requests,json,re

albumId = 15669623


headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'_xmLog=xm_1539212674445_jn3rhgnhkf162u; _ga=GA1.2.1241829775.1539212675; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1539229135,1539229209,1539284903,1539284908; device_id=xm_1542305889147_joix3se3qrkxj4',
    'Host':'www.ximalaya.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
    }
#文件名合格处理
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    return filename

# 获取章节数
def get_zhangjie(albumId):
    albumUrl = 'http://m.ximalaya.com/20100901/album/%d'% albumId
    response = requests.get(albumUrl)
    html = etree.HTML(response.text)
    jiemu_NO = html.xpath('//*[@id="container"]/div/header/ul/li[2]/a')[0].text
    jiemu_NO = re.findall(r'\d+',jiemu_NO)[0]
    page = int(jiemu_NO)//30 +1
    return page

pageNum = get_zhangjie(albumId)

No = 1
for page in range(pageNum):
    pageNum = page + 1
    url = 'https://www.ximalaya.com/revision/play/album?albumId=%d&pageNum=%d'%(albumId,pageNum)
    data = requests.get(url,headers = headers).text
    data = json.loads(data)
    msg = data['msg']
    playlist = data['data']['tracksAudioPlay']
    if No == 1:
        albumName = playlist[0]['albumName']
        albumName = ChangeFileName(albumName)
        with open(albumName +'.bat','a',encoding='utf-8') as f:
            f.writelines(['chcp 65001','\n'])
    for play in playlist:
        trackName = play['trackName']
        trackName = trackName.replace(' ','')
        trackName = trackName.replace('　','')
        src = play['src']
        with open(albumName +'.bat','a',encoding='utf-8') as f:
            f.writelines(['aria2c -o '+ str(No).zfill(4)+trackName +'.m4a ' + src,'\n'])
            No+=1

