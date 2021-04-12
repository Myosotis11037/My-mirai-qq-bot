import asyncio
import datetime
from datetime import date
from fake_useragent import UserAgent
from faker import Faker
import requests

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
    group = [766517688,862315052,875626950,729801800]
    h = datetime.datetime.now().hour
    msg = ' '
    if h == 6 or h == 23:
        ua = Faker()
        headers = {
        'cookie': "BIDUPSID=9D96E01732C84E3EF46E6D69F715EB8E; PSTM=1574597643; bdshare_firstime=1574667391465; rpln_guide=1; H_WISE_SIDS=147935_162057_156287_159609_162914_155225_161299_163303_161266_162371_159382_159937_161421_157263_161419_161970_127969_161770_160102_161958_160897_161729_162347_131423_160861_128698_161082_153149_162445_158055_160800_162169_161965_159954_160422_162474_162151_144966_162095_162187_161239_139883_158640_155530_163114_147552_162479_162267_162524_162861_162816_162642_159092_162264_162261_162155_110085_162026_163321; BAIDUID=CA1D410F7713287242D266621C18831C:FG=1; __yjs_duid=1_2f71f9689f273d49d3b607ed4bead1ca1611406958065; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33423_33582_33273_31253_26350_33544; delPer=0; PSINO=7; BAIDUID_BFESS=308E2AF32F2705030DB38E99B12C6328:FG=1; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BA_HECTOR=2kal01a58ga42h8gqt1g27n8q0r; st_key_id=17; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1612899973,1612899985,1612963100,1612963106; ab_sr=1.0.0_OTNlZDA4ZTNjNWQzYzEyZTg3NmU3ZTU2ZTM0OTYzMzM2NWFhOTgwMThmNWU4N2Y5YWExNWExOTM2ZThmM2JmMTJlOTZmZTRhYzE2ODZiOGJjMTQ4MjEyNTJkZjY1OTZlODZiZjg2NDE4MWRiZDJmZmUxNWRmN2JiZTgzM2ZmZTA=; st_data=6ff647c25e22e6e2098ddd2b4d912445ecd2b7a96a113d85893a95c7106afea705096a5203902ba371dce271f377c6fe1cf78cee29958d81bc1b2eefaafff0eb919f7810870e1562e9e0da7fd55f383a36176d3d772d68e90ff7eb8e121e5085d76aa9b6314c23eebd55995d0777b5950d21b55485d174f84dafb08ea9375a31; st_sign=8f3d7169; baidu_broswer_setup_sargarse=0; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1612963136; BDUSS=0lQdzl0LUtwRGdvSmJILTVuaDRsRjJndG9VV25rMVFnVDA5M0JjV0JKaG9ha3RnRVFBQUFBJCQAAAAAAAAAAAEAAACuIkFKc2FyZ2Fyc2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjdI2Bo3SNgZ; BDUSS_BFESS=0lQdzl0LUtwRGdvSmJILTVuaDRsRjJndG9VV25rMVFnVDA5M0JjV0JKaG9ha3RnRVFBQUFBJCQAAAAAAAAAAAEAAACuIkFKc2FyZ2Fyc2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjdI2Bo3SNgZ; STOKEN=1475d1ef2d029f121173478668e6605d6dd6dbc639869b78c0e1318306d5f9af",
        'user-Agent': str(ua.user_agent),
        'content-Type': 'application/json'
        }
        url = 'https://tieba.baidu.com/tbmall/onekeySignin1'
        param = {'ie': 'utf-8', 'tbs': 'dbcb633d0a5796b81612963177'}
        a = requests.post(url, data = param, headers = headers)
        msg = MessageChain.create([At(5980403),Plain("\n签到成功的贴吧为"+str(a.json()['data']['signedForumAmount'])+'个\n'+"签到失败的贴吧为"+str(a.json()['data']['signedForumAmountFail'])+'个')])
        await app.sendGroupMessage(372733015,msg)
        return
    elif h == 7:
        msg = "已经早上七点了！大家起床了吗？今天又是元气满满的一天呢！"
    elif h == 12:
        msg = "现在是中午十二点！吃午饭了吗？"
    elif h == 13:
        msg = "现在是下午一点！现在是午休的好时间，好好休息一下吧！"
    elif h == 18:
        msg = "现在是18点啦！准备好吃晚饭了吗？"
    elif h == 23:
        msg = "23点啦！一天的时间过得真快呢（不舍），大家一定要注意身体、养成良好的作息习惯哦！"
    
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