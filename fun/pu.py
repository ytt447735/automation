import time
import requests
import json
import datetime


def convert_cookies_to_dict(cookies):
    """
    处理cookies
    :param cookies:
    :return:
    """
    cookies = dict([l.split("=", 1) for l in cookies.replace(' ', '').split(";")])
    return cookies


def get_millisecond():
    """
       :return: 获取精确毫秒时间戳,13位
       """
    millis = int(round(time.time() * 1000))
    return millis

def get_millisecondToTim(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = date.strftime('%Y-%m-%d')
    return  formatted_date


def Get_client_code(access_token):
    client_code_url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={}'.format(access_token)
    response = requests.post(client_code_url, json={'path': 'pages/index/index'})
    client_code = response.content
    print(client_code)
