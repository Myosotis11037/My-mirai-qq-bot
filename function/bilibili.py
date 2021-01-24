import random

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

s = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

import random
import math

import requests
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.broadcast.interrupt.waiter import Waiter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}


def bvcrawler(bv):

    av = dec(bv)
    url = "https://api.bilibili.com/x/web-interface/archive/desc?aid=" + str(av) + "&page="
    d = requests.get(url, headers=headers).json()

    return d


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

