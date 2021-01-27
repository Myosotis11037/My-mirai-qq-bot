import asyncio
import datetime
from datetime import date

from graia.application import GraiaMiraiApplication, Session
from graia.application.entry import (BotMuteEvent, FriendMessage, GroupMessage,
                                     MemberMuteEvent, MemberUnmuteEvent)
from graia.application.event.lifecycle import ApplicationLaunched
from graia.application.event.messages import TempMessage
from graia.application.event.mirai import BotLeaveEventKick
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain, Quote,Face
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter

async def bell(app):
    group = [766517688,862315052,875626950]
    h = datetime.datetime.now().hour
    msg = ' '
    if h == 7:
        msg = "已经早上七点了！大家起床了吗？今天又是元气满满的一天呢！"
    elif h == 12:
        msg = "现在是中午十二点！吃午饭了吗？"
    elif h == 13:
        msg = "现在是下午一点！现在是午休的好时间，好好休息一下吧！"
    elif h == 18:
        msg = "现在是18点啦！准备好吃晚饭了吗？"
    elif h == 23:
        msg = "一天的时间过得真快呢（不舍），大家一定要注意身体、养成良好的作息习惯哦！"
    
    if msg == ' ':
        return
    for numbers in group:
        await app.sendGroupMessage(numbers,MessageChain.create([Plain(msg)]))


async def clock(app):
    while True:
        a = datetime.datetime.now()
        d = datetime.timedelta(hours=1)
        aa = datetime.time(a.hour, 0, 0, 0)
        b = datetime.datetime.combine(a.date(), aa) + d
        c = b - a
        print(a)
        print(b)
        ss = c.seconds + float('0.' + str(c.microseconds))
        print(ss)
        await asyncio.sleep(ss)
        print("时间矫正完成。当前时间：", datetime.datetime.now())
        while True:
            t = datetime.datetime.now()
            if t.minute != 0:
                print("产生分的时间误差，开始矫正", t)
                break
            asyncio.create_task(bell(app))
            if t.second != 0:
                print("产生秒的时间误差，开始矫正", t)
                break
            await asyncio.sleep(3600)
            pass