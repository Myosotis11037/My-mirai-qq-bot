import random

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

import random
import math

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

SESSDATA = "2058cc55%2C1625075012%2Ccc2ae*11"
bili_jct = "165632363f61bf53c903a3eb0c28dbac"
cookie = "SESSDATA=" + SESSDATA + "; bili_jct=" + bili_jct
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', 'cookie': cookie}


def bvcrawler(bv):

    url = "http://api.bilibili.com/x/web-interface/view?bvid=" + bv
    information = requests.get(url, headers=headers).json()
    title = information['data']['title']
    AV = information['data']['aid']
    BV = information['data']['bvid']
    view = information['data']['stat']['view']
    danmaku = information['data']['stat']['danmaku']
    reply = information['data']['stat']['reply']
    favourite = information['data']['stat']['favorite']
    coin = information['data']['stat']['coin']
    share = information['data']['stat']['share']
    like = information['data']['stat']['like']
    cover_url = information['data']['pic']

    av = dec(bv)
    url = "https://api.bilibili.com/x/web-interface/archive/desc?aid=" + \
        str(av) + "&page="
    prefile = requests.get(url, headers=headers).json()

    sstr = "标题：" + str(title) + "\n" + "AV号：AV" + \
        str(AV) + " BV号：" + str(BV) + "\n"
    sstr = sstr + "\n" + "视频简介：\n" + prefile['data']

    sstr = sstr + "\n\n" + "播放量：" + str(view) + "\n"
    sstr = sstr + "弹幕数：" + str(danmaku) + "\n"
    sstr = sstr + "回复数：" + str(reply) + "\n"
    sstr = sstr + "收藏数：" + str(favourite) + "\n"
    sstr = sstr + "投币数：" + str(coin) + "\n"
    sstr = sstr + "分享数：" + str(share) + "\n"
    sstr = sstr + "获赞数：" + str(like) + "\n\n"

    lianjie = "http://www.bilibili.com/video/" + bv
    sstr = sstr + "视频链接：\n" + lianjie

    return {"information": sstr, "cover_url": cover_url}


def avcrawler(av):
    av = av[2:]
    url = "http://api.bilibili.com/x/web-interface/view?aid=" + av
    information = requests.get(url, headers=headers).json()
    title = information['data']['title']
    AV = information['data']['aid']
    BV = information['data']['bvid']
    view = information['data']['stat']['view']
    danmaku = information['data']['stat']['danmaku']
    reply = information['data']['stat']['reply']
    favourite = information['data']['stat']['favorite']
    coin = information['data']['stat']['coin']
    share = information['data']['stat']['share']
    his_rank = information['data']['stat']['his_rank']
    like = information['data']['stat']['like']
    cover_url = information['data']['pic']

    url = "https://api.bilibili.com/x/web-interface/archive/desc?aid=" + \
        str(av) + "&page="
    prefile = requests.get(url, headers=headers).json()

    sstr = "标题：" + str(title) + "\n" + "AV号：AV" + \
        str(AV) + " BV号：" + str(BV) + "\n"
    sstr = sstr + "\n" + "视频简介：\n" + prefile['data']

    sstr = sstr + "\n\n" + "播放量：" + str(view) + "\n"
    sstr = sstr + "弹幕数：" + str(danmaku) + "\n"
    sstr = sstr + "回复数：" + str(reply) + "\n"
    sstr = sstr + "收藏数：" + str(favourite) + "\n"
    sstr = sstr + "投币数：" + str(coin) + "\n"
    sstr = sstr + "分享数：" + str(share) + "\n"
    sstr = sstr + "历史最高排行：" + str(his_rank) + "\n"
    sstr = sstr + "获赞数：" + str(like) + "\n\n"

    lianjie = "http://www.bilibili.com/video/av" + av
    sstr = sstr + "视频链接：\n" + lianjie

    return {"information": sstr, "cover_url": cover_url}


table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def dec(x):
    

    r = 0
    for i in range(6):
        r += tr[x[s[i]]]*58**i
    return (r-add) ^ xor
