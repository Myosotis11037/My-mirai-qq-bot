import random

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',}

def Touhou():
    url = "https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=166&sort_type=hot&page_size=30"
    try:
        Information = requests.get(url,headers = headers).json()
        Main = Information['data']['list'][0]
        videos = Main['items']
        sstr = "车万区周榜（每30分钟更新一次）：\n"
        for i in range(0,10):
            if i == 0: shuzi = "一"
            elif i == 1: shuzi = "二"
            elif i == 2: shuzi = "三"
            elif i == 3: shuzi = "四"
            elif i == 4: shuzi = "五"
            elif i == 5: shuzi = "六"
            elif i == 6: shuzi = "七"
            elif i == 7: shuzi = "八"
            elif i == 8: shuzi = "九"
            elif i == 9: shuzi = "十"
            sstr = sstr + "第" + shuzi + "名：" + videos[i]['name'] + "\n"
            sstr = sstr + "up主：" + videos[i]['author_name'] + "\n"
            sstr = sstr + "bv号：" + videos[i]['bvid'] + "\n"
            sstr = sstr + "视频时长：" + videos[i]['duration'] + "\n"
            sstr = sstr + "点赞数：" + videos[i]['like_count'] + "\n"
            sstr = sstr + "播放量：" + videos[i]['view_count'] + "\n"
            sstr = sstr + "视频链接：" + "https://www.bilibili.com/video/" + videos[0]['bvid']
            sstr += "\n\n"
    
    except:
        sstr = "bilibili拒绝连接！"
    return sstr
