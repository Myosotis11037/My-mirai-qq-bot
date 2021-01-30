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
global null
null = ''

def blhx():
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=33091201&host_uid=233114659&offset_dynamic_id=0&need_top=1&platform=web"
    Information = requests.get(url,headers = headers).json()
    judge = Information['data']['cards'][1]

    if judge['desc']['type'] == 2:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        try:
            if(dictInformation['item']['pictures_count'] == 1):
                pictures = dictInformation['item']['pictures'][0]['img_src']
                print(pictures)
        except:
            pictures = " "
        return {"information":dictInformation['item']['description'],"picture_url":pictures}


    elif judge['desc']['type'] == 4:
        needInformation = Information['data']['cards'][1]['card']
        dictInformation = eval(needInformation)
        pictures = " "
        return {"information":dictInformation['item']['content'],"picture_url":pictures}
    
