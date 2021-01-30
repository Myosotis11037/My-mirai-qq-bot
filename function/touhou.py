import random

import requests
from fake_useragent import UserAgent
from faker import Faker
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

from graia.application.event.messages import GroupMessage   
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

ua = Faker()
headers = {'User-Agent': str(ua.user_agent)}

def Touhou():
    url = "https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=166&sort_type=hot&page_size=30"
    try:
        Information = requests.get(url,headers = headers).json()
        Main = Information['data']['list'][0]
        videos = Main['items']
        sstr = "车万区周榜（每30分钟更新一次）：\n"
        shuzi = ["一","二","三","四","五","六","七","八","九","十"]
        for i in range(0,10):
            sstr = sstr + "第" + shuzi[i] + "名：" + videos[i]['name'] + "\n"
            sstr = sstr + "up主：" + videos[i]['author_name'] + "\n"
            sstr = sstr + "bv号：" + videos[i]['bvid'] + "\n"
            sstr = sstr + "视频时长：" + videos[i]['duration'] + "\n"
            sstr = sstr + "点赞数：" + videos[i]['like_count'] + "\n"
            sstr = sstr + "播放量：" + videos[i]['view_count'] + "\n"
            sstr = sstr + "视频链接：" + "https://www.bilibili.com/video/" + videos[i]['bvid']
            sstr += "\n\n" if i < 9 else "\n"
    except:
        sstr = "bilibili拒绝连接！"
    return sstr
