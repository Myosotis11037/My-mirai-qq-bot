import asyncio
import datetime
import json
import operator
import random
import requests
import re
import aiohttp
from lxml import etree
from re import escape
from typing import Dict, Optional
from fake_useragent import UserAgent
from faker import Faker

from graia.application import GraiaMiraiApplication, Session
from graia.application.entry import (BotMuteEvent, FriendMessage, GroupMessage,
                                     MemberMuteEvent, MemberUnmuteEvent)
from graia.application.event.lifecycle import ApplicationLaunched
from graia.application.event.messages import TempMessage
from graia.application.event.mirai import BotLeaveEventKick
import graia.application.message.elements.internal as Msg_element

from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain, Quote,Face,Xml
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass


async def song(app,inc,group,member,msg):
    ua = Faker()
    song_name = msg[3:]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', 'content-type': 'application/x-www-form-urlencoded; charset=utf-8', 'cookie': "WM_TID=1VRbiW7aQ5hBFVEEQBM%2FOr1gD39dKN2w; NMTID=00O_jMOLpgia551tk60jDuGpwdl4xEAAAF35DclxA; mail_psc_fingerprint=eb5dc1ca00b8e87271f138179a23da7a; nts_mail_user=18007411263@163.com:-1:1; _ntes_nnid=21be7b2802bdbcc31e429aec7b260faa,1614441555861; _ntes_nuid=21be7b2802bdbcc31e429aec7b260faa; Qs_lvt_382223=1614477403; Qs_pv_382223=4341904008701340000; _ga=GA1.1.126750718.1614477403; _ga_C6TGHFPQ1H=GS1.1.1614477403.1.0.1614477412.0; ntes_kaola_ad=1; NTES_PASSPORT=7J.2NBisllL6hshwfG.yx27QbFN5xD8cPch2_1VsTCNfgN.agb3pG94aoLnB247RbEnhksdxMYlu0kVatOsAmNY3gtw5OLd50Qmp6WqNckAB67lMuYZZwxJ2itFon_n17zeQFJLGkb6YDpV5MEMOXnnu7oyP8nVpAJyIMUmhmkPLSP0x84NEzTWfqztB9L_CX; P_INFO=m18007411263_1@163.com|1617792265|1|mail163|00&99|shh&1614441549&mail163#shh&null#10#0#0|180263&1||18007411263@163.com; _iuqxldmzr_=32; WEVNSM=1.0.0; WNMCID=bmlbdx.1618302416734.01.0; JSESSIONID-WYYY=W1gIMV4Xa4dtOAKwBNzCnE68EsMI4ukCmpDTRsDiJFC1gZ6cJlCtB5N819cx5ES5geqZuTrXXo2ZF%2F8FrWCVHZU%2BTkxVJ4lug%5C8%2FGniWZRDZPfmBp5EJV0dN90yJFatAQAfv9ndtpuZNdlNfV%2B%5CAKD5SEl4MDaYOCwjp2NX%2BTRyyfebF%3A1618310859998; WM_NI=VKwvdTsQnySUgUjelXx9bb5dSLV8zMkAo1DXVWWZpBKeQds661fan%2FP%2FYRKb55dwWS%2BPLi%2FqR5rV%2BGJfGWTAgoj53zJfLwHcGzOw3gdfsgOhPeA1T3PrjnRICnHg19ZUMkQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8ad37a97aebe84c42591b48aa3d55f978a9b85b53c898996d3f8498c99c090b22af0fea7c3b92a9695b997e760b18fa29ad25fa58ba686ef54bce7ae83b87091949ad9f947a99fa1d2c754968999bbf34a89bb9f85f23ef6efaa82ed2594f197b3ca6af7ebac98d659e990848aae7b92ebbeb7aa4d8aba89b8d74ba5b1a6d6b2728aba8498cb6985a68198b26da8babd88ce6494bb8fd2d73994aea68fd14381b28888b4339a8b838cd437e2a3"}
    api = "http://music.163.com/api/search/get/web?csrf_token="
    name = "hlpretag=&hlposttag=&s=" + song_name + "&type=1&offset=0&total=true&limit=10"
    url = api + name
    async with aiohttp.ClientSession() as session:
        async with session.get(url = url) as resp:
            data_json = await resp.read()
    data_json = json.loads(data_json)

    if data_json['result']['songCount'] == 0:
        await app.sendGroupMessage(group,MessageChain.create([Plain('找不到该歌曲'),Face(faceId=107)]))
        return

    search_result = "搜索结果为：\n"
    if data_json['result']['songCount'] >= 10:
        loop_count = 10
    else:
        loop_count = data_json['result']['songCount']
    for i in range(loop_count):
        search_result += str(i+1) + "、歌曲名：" + str(data_json['result']['songs'][i]['name']) + "  歌手：" + data_json['result']['songs'][i]['artists'][0]['name']
        if i < 9:
            search_result += '\n'
    msg_str = search_result
    mention = "  有多首相关歌曲，请输入数字【1-10】来选择你要播放的歌曲~\n" + msg_str
    msg = MessageChain.create([At(member.id),Plain(mention)])
    await app.sendGroupMessage(group,msg)

    @Waiter.create_using_function([GroupMessage])
    async def waiter(event: GroupMessage, waiter_group: Group, waiter_member: Member, waiter_message: MessageChain):
        if waiter_group.id == group.id and waiter_member.id == member.id:
            if is_int(waiter_message.asDisplay()):
                location = int(waiter_message.asDisplay()) - 1
                print(location)
                if location >= data_json['result']['songCount'] or location < 0 or location >= 10:
                    await app.sendGroupMessage(group, MessageChain.create([Plain('没有该歌曲'),Face(faceId=107)]))
                    return event
                msg = MessageChain.create([Plain("https://y.music.163.com/m/song/" + str(data_json['result']['songs'][location]['id']) + "/?userid=335141010&app_version=8.1.80")])
                print(msg)
                await app.sendGroupMessage(group,msg)

            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain('没有该歌曲'),Face(faceId=107)]))
            return event
    await inc.wait(waiter)