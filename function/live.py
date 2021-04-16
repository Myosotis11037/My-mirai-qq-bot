import random
import os
import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain,Face
from graia.broadcast.interrupt.waiter import Waiter

import random
import math

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

fr = open("./cookie/cookie.txt", encoding='utf-8')
cookie = fr.read()
fr.close()
token = "4409a8f84719c8b946b9c4a3da3e3568"

async def getlive(app, group, member):
    url = "https://api.live.bilibili.com/room/v1/Room/startLive"
    headers = {"cookie": str(cookie)}
    data = {"room_id": "22431055", "csrf_token": token,
            "csrf": token, "area_v2": "235", "platform": "pc"}
    r = requests.post(url, data, headers=headers)
    print(r.json())
    addr = r.json()["data"]["rtmp"]["addr"]
    code = r.json()["data"]["rtmp"]["code"]
    if (r.json()["data"]["status"] == "LIVE"):
        if member.id == 5980403:
            await app.sendFriendMessage(member.id, MessageChain.create([Plain(addr)]))
            await app.sendFriendMessage(member.id, MessageChain.create([Plain(code)]))
        else:
            await app.sendTempMessage(group.id, member.id, MessageChain.create([Plain(addr)]))
            await app.sendTempMessage(group.id, member.id, MessageChain.create([Plain(code)]))
        await app.sendGroupMessage(group, MessageChain.create([Plain("直播间开启成功")]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain("直播间开启失败，可能是cookie过期")]))

async def liveend(app, group):
    url = "https://api.live.bilibili.com/room/v1/Room/stopLive"
    headers = {"cookie": cookie}
    data = {"room_id": "22431055", "csrf_token": token,
            "csrf": token, "platform": "pc"}
    r = requests.post(url, data, headers=headers)
    if (r.json()["data"]["status"] == "PREPARING"):
        await app.sendGroupMessage(group, MessageChain.create([Plain("直播间关闭成功")]))

async def livechange(app, group, msg: str):
    text = msg.split(' ')
    if(len(text) < 2):
        return
    title = text[1]
    for i in range(2, len(text)):
        title = title + ' ' + text[i]

    url = "https://api.live.bilibili.com/room/v1/Room/update"
    headers = {"cookie": cookie}
    data = {"room_id": "22431055", "csrf_token": token,
            "csrf": token, "title": title}
    r = requests.post(url, data, headers=headers)
    if (r.json()["msg"] == "ok"):
        await app.sendGroupMessage(group, MessageChain.create([Plain("直播间标题已更改为：\n" + title)]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain("直播间标题更改失败，可能是cookie过期")]))


