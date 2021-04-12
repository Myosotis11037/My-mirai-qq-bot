import asyncio
import datetime
import json
import operator
import random
import requests
import re
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

from function.bilibili import bvcrawler
from function.bilibili import avcrawler
from function.time import bell,clock
from function.touhou import Touhou
from function.blhx import blhx
from function.blhx import blhxpush

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="HolaisanKaguya", # 填入 authKey
        account=3304895821, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

pattern = re.compile(r'BV1[1-9A-NP-Za-km-z]{9}')
@bcc.receiver(GroupMessage)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    if Msg_element.Xml in message:
        xml_msg = etree.fromstring(message.get(Msg_element.Xml)[0].xml.encode('utf-8'))
        url = xml_msg.xpath('/msg/@url')[0]
        result = re.search(pattern, url)
    else:
        result = re.search(pattern,message.asDisplay())

    
    if result != None:
        BVname = result.group()
        print(BVname)
        videoInformation = bvcrawler(BVname)
        await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))


    if message.has(At):
        flag = 0
        for at in message.get(At):
            if at.target == 5980403:
                flag = 1
        if flag == 0:
            return
        else:
            msg = message.asSerializationString()
            message_a = MessageChain.create([Plain("消息监听：\n%s（%d）在群%s（%d）中对我说：\n%s" % (member.name,member.id,group.name,group.id,message.asDisplay()))])
            message_b = message.asSendable()
            message_a.plus(message_b)
            for i in range(0, len(message_a.__root__)):
                if message_a.__root__[i].type == 'At':
                    message_a.__root__[i] = Plain(
                        message_a.__root__[i].display)

            
            await app.sendFriendMessage(5980403,message_a)



    if message.asDisplay() == "help":
        sstr = "目前已经公开的功能有：" + "\n\n" 
        sstr += "①打招呼功能，输入hi说不定可以得到妹妹的回应哦~" + "\n\n"
        sstr += "②查bv号和av号的功能，能够显示视频的详细信息~" + "\n\n"
        sstr += "③随机提供涩图的功能，输入‘色图时间’或者‘来点涩图’就可以随机发送一张图片了~" + "\n\n"
        sstr += "④整点报时功能~\n\n"
        sstr += "⑤提供b站车万区周榜功能~\n\n"
        sstr += "⑥碧蓝航线实时推送功能，并且输入'碧蓝航线最新动态'可以得到碧蓝航线官方账号发送的最新动态哦~\n\n"
        sstr += "⑦输入'lex凉了没'可以获取lex最新掉分情况~\n"
        sstr += "凛夜sama赛高！（不要忘了所有的功能都是凛夜亲手敲的代码哦）"    
        await app.sendGroupMessage(group,MessageChain.create([Plain(sstr)]))

    if message.asDisplay() == "hi":
        if(member.id == 5980403):
            await app.sendGroupMessage(group,MessageChain.create([At(5980403),Plain(" 哥哥爱死你了mua")]))
        elif(member.id == 349468958):
            await app.sendGroupMessage(group,MessageChain.create([Plain("哥哥我也爱你呢❤")]))
        elif(member.id == 865734287):
            await app.sendGroupMessage(group,MessageChain.create([Plain("mu..(害怕)mua?"),Face(faceId=111)]))
        elif(member.id == 744938425):
            await app.sendGroupMessage(group,MessageChain.create([At(744938425),Plain(" 欧尼酱要吃饭呢，要洗澡呢，还是要先吃我呢"),Face(faceId=111)]))
        else:
            await app.sendGroupMessage(group,MessageChain.create([At(member.id),Plain("hi~")]))
    
    if message.asDisplay() == "晚安":
        if(member.id == 5980403):
            await app.sendGroupMessage(group,MessageChain.create([At(5980403),Plain(" 哥哥晚安"),Face(faceId=75)]))
        else:
            await app.sendGroupMessage(group,MessageChain.create([At(member.id),Plain(" 晚安~")]))

    if message.asDisplay() == "草" or message.asDisplay() == "艹":
        if random.random() <= 0.25:
            await app.sendGroupMessage(group,MessageChain.create([Plain("草")]))
        else:
            return

    if(member.id != 2083664136 and member.id != 2079373402):
        if message.asDisplay().startswith("BV"):
            videoInformation = bvcrawler(message.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))
        elif message.asDisplay().startswith("AV") or message.asDisplay().startswith("av"):
            videoInformation = avcrawler(message.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))

    if message.asDisplay() == "色图时间" or message.asDisplay() == "来点涩图" or message.asDisplay() == "来点色图":
        url = "https://api.nmb.show/1985acg.php"

        try:
            await app.sendGroupMessage(group, MessageChain.create([Image.fromNetworkAddress(url)]))
        except:
            await app.sendGroupMessage(group,MessageChain.create([Plain("该图片无法显示qwq"),Face(faceId=107)]))

    if message.asDisplay() == "车万周榜" or message.asDisplay() == "东方周榜":
        msg = Touhou()
        await app.sendGroupMessage(group,MessageChain.create([Plain(msg)]))
    
    if message.asDisplay() == "维护" and member.id == 5980403:
        msg = "就算是机器人的妹妹我也要休息了呢qwq，凛夜哥哥要对我进行功能维护了，大家好好期待吧~"
        groups = [372733015,766517688,875626950,862315052,729801800]
        for group in groups:
            await app.sendGroupMessage(group,MessageChain.create([Plain(msg)]))
    
    if message.asDisplay() == "停止维护" and member.id == 5980403:
        msg = "凛夜哥哥对我的维护已经结束了，我又可以继续被大家正常使用了呢~（羞涩）"
        groups = [372733015,766517688,875626950,862315052,729801800]
        for group in groups:
            await app.sendGroupMessage(group,MessageChain.create([Plain(msg)]))


    if message.asDisplay() == "碧蓝航线最新动态":
        await blhx(app,group)

    if message.asDisplay() == "lex凉了没" or message.asDisplay() == "lex":
        lexurl = "https://api.bilibili.com/x/relation/stat?vmid=777536"
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', }
        msg = requests.get(lexurl, headers = headers).json()
        followers = msg['data']['follower']
        string = "lex的粉丝数已经掉到" + str(followers) + "了~"
        await app.sendGroupMessage(group,MessageChain.create([Plain(string)]))

    if member.id == 5980403 and message.asDisplay() == '贴吧签到':
        ua = Faker()
        headers = {
        'cookie': "BIDUPSID=9D96E01732C84E3EF46E6D69F715EB8E; PSTM=1574597643; bdshare_firstime=1574667391465; rpln_guide=1; H_WISE_SIDS=147935_162057_156287_159609_162914_155225_161299_163303_161266_162371_159382_159937_161421_157263_161419_161970_127969_161770_160102_161958_160897_161729_162347_131423_160861_128698_161082_153149_162445_158055_160800_162169_161965_159954_160422_162474_162151_144966_162095_162187_161239_139883_158640_155530_163114_147552_162479_162267_162524_162861_162816_162642_159092_162264_162261_162155_110085_162026_163321; BAIDUID=CA1D410F7713287242D266621C18831C:FG=1; __yjs_duid=1_2f71f9689f273d49d3b607ed4bead1ca1611406958065; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33423_33582_33273_31253_26350_33544; delPer=0; PSINO=7; BAIDUID_BFESS=308E2AF32F2705030DB38E99B12C6328:FG=1; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BA_HECTOR=2kal01a58ga42h8gqt1g27n8q0r; st_key_id=17; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1612899973,1612899985,1612963100,1612963106; ab_sr=1.0.0_OTNlZDA4ZTNjNWQzYzEyZTg3NmU3ZTU2ZTM0OTYzMzM2NWFhOTgwMThmNWU4N2Y5YWExNWExOTM2ZThmM2JmMTJlOTZmZTRhYzE2ODZiOGJjMTQ4MjEyNTJkZjY1OTZlODZiZjg2NDE4MWRiZDJmZmUxNWRmN2JiZTgzM2ZmZTA=; st_data=6ff647c25e22e6e2098ddd2b4d912445ecd2b7a96a113d85893a95c7106afea705096a5203902ba371dce271f377c6fe1cf78cee29958d81bc1b2eefaafff0eb919f7810870e1562e9e0da7fd55f383a36176d3d772d68e90ff7eb8e121e5085d76aa9b6314c23eebd55995d0777b5950d21b55485d174f84dafb08ea9375a31; st_sign=8f3d7169; baidu_broswer_setup_sargarse=0; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1612963136; BDUSS=0lQdzl0LUtwRGdvSmJILTVuaDRsRjJndG9VV25rMVFnVDA5M0JjV0JKaG9ha3RnRVFBQUFBJCQAAAAAAAAAAAEAAACuIkFKc2FyZ2Fyc2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjdI2Bo3SNgZ; BDUSS_BFESS=0lQdzl0LUtwRGdvSmJILTVuaDRsRjJndG9VV25rMVFnVDA5M0JjV0JKaG9ha3RnRVFBQUFBJCQAAAAAAAAAAAEAAACuIkFKc2FyZ2Fyc2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjdI2Bo3SNgZ; STOKEN=1475d1ef2d029f121173478668e6605d6dd6dbc639869b78c0e1318306d5f9af",
        'user-Agent': str(ua.user_agent),
        'content-Type': 'application/json'
        }
        url = 'https://tieba.baidu.com/tbmall/onekeySignin1'
        param = {'ie': 'utf-8', 'tbs': 'dbcb633d0a5796b81612963177'}
        a = requests.post(url, data = param, headers = headers)
        msg = MessageChain.create([Plain("签到成功的贴吧为"+str(a.json()['data']['signedForumAmount'])+'个\n'+"签到失败的贴吧为"+str(a.json()['data']['signedForumAmountFail'])+'个')])
        await app.sendGroupMessage(group,msg)



ua = Faker()
headers = {'User-Agent': str(ua.user_agent)}
global null
null = ''
groups = [372733015,875626950,766517688,862315052,729801800]

@bcc.receiver(ApplicationLaunched)
async def repeat(app:GraiaMiraiApplication):
    asyncio.create_task(clock(app))
    blhxurl = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(blhxurl,headers = headers).json()
    preTimestamp = Information['data']['cards'][1]['desc']['timestamp']
    asyncio.create_task(blhxpush(app,preTimestamp))
    


app.launch_blocking()