import asyncio
import datetime
import json
import operator
import random
import requests
import re
import aiohttp
import os
from lxml import etree
from re import escape
from typing import Dict, Optional
from fake_useragent import UserAgent
from faker import Faker
from pathlib import Path


from graia.application import GraiaMiraiApplication, Session
from graia.application.entry import (BotMuteEvent, FriendMessage, GroupMessage,
                                     MemberMuteEvent, MemberUnmuteEvent,MemberPerm)
from graia.application.event.lifecycle import ApplicationLaunched
from graia.application.event.messages import TempMessage
from graia.application.event.mirai import BotLeaveEventKick
import graia.application.message.elements.internal as Msg_element

from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain, Quote,Face,Xml,Voice
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter

from function.bilibili import bvcrawler
from function.bilibili import avcrawler
from function.time import bell,clock
from function.touhou import Touhou
from function.blhx import blhx
from function.blhx import blhxpush
from function.song import song
from function.danmaku import livewrite, entrance, get_info
from function.live import getlive,liveend,livechange

loop = asyncio.get_event_loop()
info = {}

ua = Faker()
headers = {'User-Agent': str(ua.user_agent)}
global null
null = ''
groups = [372733015,875626950,766517688,862315052,729801800]
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://42.193.102.81:8080", # 填入 httpapi 服务运行的地址
        authKey="myon759572692", # 填入 authKey
        account=2157510360, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
inc = InterruptControl(bcc)

bvpattern = re.compile(r'BV1[1-9A-NP-Za-km-z]{9}')
@bcc.receiver(GroupMessage)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):

    url = ""
    b23_url = ""  # 先申请好两种要用的url
    if Msg_element.Xml in message:
        xml = message.get(Xml)
        xml_msg = etree.fromstring(message.get(Msg_element.Xml)[0].xml.encode('utf-8')) #将xml进行解码
        url = xml_msg.xpath('/msg/@url')[0] #这是xml中包含bv号的链接
        result = re.search(bvpattern, url)  #进行bv号的一个匹配
    else:
        result = re.search(bvpattern,message.asDisplay())   #说明是纯文本，直接找bv号
    
    if result != None:  #匹配到了的情况：说明是用电脑端的链接分享的
        BVname = result.group()
        print(BVname)
        videoInformation = bvcrawler(BVname)
        await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))
    else:   #没有匹配到bv号然而又是xml，说明这不是电脑端分享的链接，而是iphone分享的链接，这里的url是b23短链接
        if url != "":   #因为url初值是空，所以这里做一个判断避免每一次输入一个信息就进行查找
            b23_url = url
            resp = requests.get(b23_url,allow_redirects=False)  #向b23短链接发送请求，然后阻止其进行重定向到网站上去
            redirect_url = resp.headers.get('Location') #得到重定向后的url
            result = re.search(bvpattern, redirect_url) #得到重定向后的bv号
            if result != None:
                BVname = result.group()
                print(BVname)
                videoInformation = bvcrawler(BVname)
                await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))

    if Msg_element.App in message:  #说明是用手机分享的，是一个json格式的消息，我们可以从中解码得到b23短链接
        json_msg = json.loads(message.get(Msg_element.App)[0].content)  #这里的json格式要这样解码
        name = json_msg['desc']
        if name == "哔哩哔哩":  #如果这里的name叫哔哩哔哩，那说明是手机客户端分享的小程序
            b23_url = json_msg['meta']['detail_1']['qqdocurl']  #b23_url此时在这里
        else:   #这里的name不是叫哔哩哔哩了，准确来说是为空，那说明是ipad的HD客户端分享的小程序
            b23_url = json_msg['meta']['news']['jumpUrl']   #b23_url此时又是在这里
        resp = requests.get(b23_url,allow_redirects=False)  #和上面一样的http302拦截，然后得到bv号
        redirect_url = resp.headers.get('Location')
        result = re.search(bvpattern, redirect_url)
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
        sstr += "②查bv号和av号的功能，并且能够解析任何形式分享的b站视频，能够显示视频的详细信息~" + "\n\n"
        sstr += "③随机提供涩图的功能，输入‘色图时间’或者‘来点涩图’就可以随机发送一张图片了~" + "\n\n"
        sstr += "④整点报时功能~\n\n"
        sstr += "⑤提供b站车万区周榜功能~\n\n"
        sstr += "⑥碧蓝航线实时推送功能，并且输入'碧蓝航线最新动态'可以得到碧蓝航线官方账号发送的最新动态哦~\n\n"
        sstr += "⑦点歌功能。输入【点歌 xxx】就可以查找到你喜欢的歌曲哦~\n"
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
        if message.asDisplay().startswith("AV") or message.asDisplay().startswith("av"):
            videoInformation = avcrawler(message.asDisplay())
            await app.sendGroupMessage(group,MessageChain.create([Image.fromNetworkAddress(videoInformation['cover_url']),Plain(videoInformation['information'])]))

    if message.asDisplay() == "色图时间" or message.asDisplay() == "来点涩图" or message.asDisplay() == "来点色图":
        url = "https://api.nmb.show/1985acg.php"
        conn=aiohttp.TCPConnector(ssl=False)
        async with aiohttp.request('GET', url, connector=conn) as resp:
            content = await resp.read()
        try:
            await app.sendGroupMessage(group, MessageChain.create([Image.fromUnsafeBytes(content)]))
        except:
            await app.sendGroupMessage(group,MessageChain.create([Plain("该图片无法显示qwq"),Face(faceId=107)]))
    
    if message.asDisplay() == "来点辉夜" or message.asDisplay() == "辉夜图":
        kaguyaDir = "./Kaguya"
        kaguyaNames = []
        for parent, dirnames, filenames in os.walk(kaguyaDir):
            kaguyaNames = filenames
        x = random.randint(0,len(kaguyaNames) - 1)
        pictureLocation = kaguyaDir + "/" + kaguyaNames[x]
        await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(pictureLocation)]))
        

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

    if message.asDisplay().startswith("点歌"):
        await song(app,inc,group,member,message.asDisplay())

    # if member.id == 5980403 and message.asDisplay().startswith("订阅直播 "):
    #     room_id = message.asDisplay().replace("订阅直播 ",'')
    #     global info

    #     Localpath = 'data/data.json'
    #     data = {}
    #     fr = open(Localpath,encoding = 'utf-8')
    #     data = json.load(fr)
    #     fr.close

    #     for i in data['data']:
    #         if room_id == str(i['room_id']):
    #             if group.id in i['group']:
    #                 await app.sendGroupMessage(group,MessageChain.create([Plain("这个直播已经在订阅列表中了哦~")]))
    #                 break
            
    #         else:
    #             try:
    #                 if not room_id in info:
    #                     info['room_id'] = asyncio.create_task(entrance(app,room_id))
    #                 info = get_info(room_id)
    #                 await app.sendGroupMessage(group, MessageChain.create([Plain("开启对%s(%d)的直播间订阅" % (info['user'], info['uid']))]))
    #                 livewrite(group.id, int(room_id))
    #             except:
    #                 await app.sendGroupMessage(group, MessageChain.create([Plain("开启直播订阅失败，请检查房间号")]))
    #                 del info['room_id']

    if message.asDisplay() == "直播help":
        help_str = "目前红群直播的开启功能已经基本上由凛夜哥哥写完了，下面是大概的使用方法~\n"
        help_str += "首先，直播开启的权限是由白名单决定的，白名单存储在服务器上，只能由红群和tfcc群的管理员以及凛夜本人进行添加。添加方法为：【白名单添加 qq号】。管理员必须要注意的是：添加完qq号以后，请马上输入【添加id 名字】来添加qq号成员对应的名字，不然白名单可能会无法正常运行！\n"
        help_str += "然后开启直播的方法是【开始直播】。只有白名单上的成员才能开启直播哦！如果你想查看白名单的成员，请输入【直播白名单】，或者是之前莉莉白的查看方式【！白名单】。这里凛夜哥哥是为了迎合大家之前的习惯做的~\n"
        help_str += "如果需要修改白名单，请发送【白名单删除 qq号】。请管理员注意，删除完白名单上的qq号以后请务必删除qq号对应的id！方法为【删除id 名字】！\n"
        help_str += "如果有人在开启直播，其他白名单上的成员还发送了【开始直播】，那么机器人会提醒你有人在使用直播~如果使用直播的人需要下线，请发送【关闭直播】。而且关闭直播的权限只有开启直播的本人有哦~\n"
        help_str += "在进行tfcc比赛时可能会需要随时更改直播标题，请发送【修改直播标题 目标名字】即可~"
        await app.sendGroupMessage(group,MessageChain.create([Plain(help_str)]))

    if message.asDisplay().startswith("白名单添加 "):
        memper = member.permission
        memper = str(memper)
        if (group.id == 182721157 or group.id == 1158449372 or group.id == 431987102 or group.id == 909918392) and (memper == "MemberPerm.Owner" or memper == "MemberPerm.Administrator" or member.id == 5980403):
            identification = message.asDisplay().replace("白名单添加 ",'')
            with open("./data/authority.txt",'r+') as autho:
                exist_IDs = autho.readlines()
                for i in range(len(exist_IDs)):
                    exist_IDs[i] = exist_IDs[i].replace('\n','')
                    if identification == exist_IDs[i]:
                        await app.sendGroupMessage(group,MessageChain.create([Plain("白名单上已经有该成员了！")]))
                        return
                autho.write(identification)
                autho.write('\n')
                autho.close()
            await app.sendGroupMessage(group,MessageChain.create([Plain("白名单添加成功！")]))
    
    if message.asDisplay().startswith("添加id "):
        memper = member.permission
        memper = str(memper)
        if (group.id == 182721157 or group.id == 1158449372 or group.id == 431987102 or group.id == 909918392) and (memper == "MemberPerm.Owner" or memper == "MemberPerm.Administrator" or member.id == 5980403):
            with open("./data/authoid.txt",'a') as temp_name:
                temp_identification = message.asDisplay().replace("添加id ",'')
                print(temp_identification)
                temp_name.write(temp_identification)
                temp_name.write('\n')
                temp_name.close()
            await app.sendGroupMessage(group,MessageChain.create([Plain("白名单id添加成功！")]))

    if message.asDisplay().startswith("白名单删除 "):
        memper = member.permission
        memper = str(memper)
        if (group.id == 182721157 or group.id == 1158449372 or group.id == 431987102 or group.id == 909918392) and (memper == "MemberPerm.Owner" or memper == "MemberPerm.Administrator" or member.id == 5980403):
            identificate = message.asDisplay().replace("白名单删除 ",'')
            target_IDs = ['0']
            with open("./data/authority.txt",'r+',encoding = 'utf-8') as aut:
                target_IDs = aut.readlines()
                where_flag = 0
                for i in range(len(target_IDs)):
                    if identificate == target_IDs[i].replace('\n',''):
                        target_IDs.pop(i)
                        where_flag = 1
                        break
                aut.close()
            if where_flag == 0:
                await app.sendGroupMessage(group,MessageChain.create([Plain("白名单上没有该成员~")]))
            else:
                with open("./data/authority.txt",'w',encoding = 'utf-8') as real_aut:
                    real_aut_content = ""
                    for i in range(len(target_IDs)):
                        real_aut_content += target_IDs[i]
                    real_aut.write(real_aut_content)
                    real_aut.close()
                await app.sendGroupMessage(group,MessageChain.create([Plain("删除成功！")]))

    if message.asDisplay().startswith("删除id "):
        memper = member.permission
        memper = str(memper)
        if (group.id == 182721157 or group.id == 1158449372 or group.id == 431987102 or group.id == 909918392) and (memper == "MemberPerm.Owner" or memper == "MemberPerm.Administrator" or member.id == 5980403):
            identificate_name = message.asDisplay().replace("删除id ",'')
            target_name = ['0']
            with open("./data/authoid.txt",'r+',encoding = 'utf-8') as nam:
                target_name = nam.readlines()
                which_flag = 0
                for i in range(len(target_name)):
                    if identificate_name == target_name[i].replace('\n',''):
                        target_name.pop(i)
                        which_flag = 1
                        break
                nam.close()
            if which_flag == 0:
                await app.sendGroupMessage(group,MessageChain.create([Plain("你删除了错误的id！")]))
            else:
                with open("./data/authoid.txt",'w',encoding = 'utf-8') as real_nam:
                    real_nam_content = ""
                    for i in range(len(target_name)):
                        real_nam_content += target_name[i]
                    real_nam.write(real_nam_content)
                    real_nam.close()
                await app.sendGroupMessage(group,MessageChain.create([Plain("id删除成功！")]))

    if message.asDisplay().startswith("角色曲 "):
        character = message.asDisplay().replace('角色曲 ','')
        with open("./data/touhou.json",encoding = 'utf-8') as touhou_characters_file:
            touhou_characters = json.load(touhou_characters_file)
            try:
                touhou_music = touhou_characters[character]
                touhou_characters_file.close()
            except:
                await app.sendGroupMessage(group,MessageChain.create([Plain("没有该角色曲！")]))
                touhou_characters_file.close()
                return
        music_file = './voice/' + touhou_music + '.silk' 
        print(music_file)
        await app.sendGroupMessage(group,MessageChain.create([Voice.fromLocalFile(0,filepath=Path(music_file))]))
            

                

    if (message.asDisplay() == "！白名单" or message.asDisplay() == "查看白名单") and (group.id == 182721157 or group.id == 1158449372 or group.id == 431987102 or group.id == 909918392) :
        IDs = ['0']
        msg_str = "白名单如下：\n"
        with open("./data/authority.txt",encoding = 'utf-8') as auth:
            with open("./data/authoid.txt",encoding = 'utf-8') as authname:
                IDs = auth.readlines()
                Names = authname.readlines()
                for i in range(len(IDs)):
                    msg_str = msg_str + Names[i].replace('\n','') + "(" + IDs[i].replace('\n','') + ")"
                    if i < len(IDs) - 1:
                        msg_str += '\n'
        await app.sendGroupMessage(group,MessageChain.create([Plain(msg_str)]))

    if message.asDisplay() == "开始直播" or message.asDisplay() == "关闭直播" or message.asDisplay().startswith("修改直播标题"):
        IDs = ['0']
        with open("./data/authority.txt",encoding = 'utf-8') as auth:
            IDs = auth.readlines()
            for i in range(len(IDs)):
                IDs[i] = IDs[i].replace('\n','')

        if not str(member.id) in IDs:
            await app.sendGroupMessage(group,MessageChain.create([At(member.id),Plain("  你无权开启直播，请向管理员申请添加白名单^-^")]))
            return
        else:
            if message.asDisplay() == "开始直播":
                Localpath = './data/live.json'
                live_info = {}
                fr = open(Localpath, encoding = 'utf-8')
                live_info = json.load(fr)
                fr.close()
                if live_info['live_status'] == 1:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id),Plain("  已经有人在使用直播间了"),Face(faceId=111)]))
                    return
                else:
                    live_info['member_id'] = member.id
                    live_info['group_id'] = group.id
                    live_info['live_status'] = 1
                    with open(Localpath, "w") as fw:
                        jsObj = json.dumps(live_info)
                        fw.write(jsObj)
                        fw.close()
                    await getlive(app, group, member)

            if message.asDisplay() == "关闭直播" or message.asDisplay() == "停止直播":
                Localpath = './data/live.json'
                live_info = {}
                fr =  open(Localpath, encoding = 'utf-8')
                live_info = json.load(fr)
                fr.close()
                if live_info['member_id'] != member.id or live_info['group_id'] != group.id:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id),Plain("  你无权关闭直播"),Face(faceId=111)]))
                    return
                elif live_info['live_status'] == 0:
                    await app.sendGroupMessage(group, MessageChain.create([At(member.id),Plain("  直播间现在是关闭状态哦~请发送'开始直播'来申请直播!")]))
                else:
                    live_info['live_status'] = 0
                    with open(Localpath, "w") as fw:
                        jsObj = json.dumps(live_info)
                        fw.write(jsObj)
                        fw.close()
                    await liveend(app, group)

            if message.asDisplay().startswith("修改直播标题"):
                await livechange(app, group, message.asDisplay())





@bcc.receiver(ApplicationLaunched)
async def repeat(app:GraiaMiraiApplication):
    asyncio.create_task(clock(app))
    blhxurl = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(blhxurl,headers = headers).json()
    preTimestamp = Information['data']['cards'][1]['desc']['timestamp']
    asyncio.create_task(blhxpush(app,preTimestamp))

    # print(os.getcwd()) # 获取当前工作目录路径
    # print(os.path.abspath('.')) # 获取当前工作目录路径

    # global info
    # Localpath = './My-mirai-qq-bot/data/data.json'
    # data = {}
    # fr = open(Localpath, encoding='utf-8')

    # data = json.load(fr)
    # fr.close()
    # for i in data["data"]:
    #     info[str(i['room_id'])] = asyncio.create_task(
    #         entrance(app, str(i['room_id'])))
    # pass

app.launch_blocking()