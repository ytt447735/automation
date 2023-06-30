import requests
import time
import json
from urllib import parse

from fun.pu import get_millisecond


class wps:
    def __init__(self, csrftoken, wps_sid):
        self.Referer = 'https://servicewechat.com/wx2f333d84a103825d/140/page-frame.html'
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6919'
        self.service_id = 'zt_clock_in'
        self.request_id = 'zt_clock_in_493528159'
        self.client_code = '0a1YllGa1yNyiF0hwcJa1p7WlN1YllG6'
        # 0c1nWK1w3J8nB03The2w3sB4FJ3nWK1V
        # 0a1kxw0w3cuzC03zzF2w3kYlNI1kxw0b
        # 0a1BaDFa123eiF0Y1sJa1x9a9P0BaDF3
        # 0c1cKYZv3LE7D03mcJ0w36gljX3cKYZ9
        self.CSRFToken = csrftoken
        self.wps_sid = wps_sid

    def GetCheck(self):
        '''
        获取个人资料
        :return:
        '''
        url = "https://account.wps.cn/p/auth/check"
        payload = "{}"
        headers = {
            'Referer': self.Referer,
            'User-Agent': self.UA,
            'X-CSRFToken': self.CSRFToken,
            'Cookie': f'csrftoken={self.CSRFToken};wps_sid={self.wps_sid}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        j = json.loads(response.text)
        if j['result'] == 'ok':
            self.request_id = f'zt_clock_in_{str(j["userid"])}'
            return j
        return False

    def GetCode(self):
        '''
        获取or刷新 验证码
        :return:
        '''
        url = f"https://vipapi.wps.cn/vas_risk_system/v1/captcha/image?service_id={self.service_id}&t={str(get_millisecond())}&request_id={self.request_id}"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'User-Agent': self.UA
        }
        # print(url)
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)

    def SendCode(self):
        '''
        迟到打卡
        :return:
        '''
        XY = ['38.5,44', '108.5,44', '178.5,44', '248.5,44', '318.5,44']
        url = "https://vipapi.wps.cn/vas_risk_system/v1/captcha/fetch_postion"
        payload = '--XXX\n'
        payload = payload + 'Content-Disposition: form-data; name="service_id"\n'
        payload = payload + '\n'
        payload = payload + f'{self.service_id}\n'
        payload = payload + '--XXX\n'
        payload = payload + 'Content-Disposition: form-data; name="request_id"\n'
        payload = payload + '\n'
        payload = payload + f'{self.request_id}\n'
        payload = payload + '--XXX\n'
        payload = payload + 'Content-Disposition: form-data; name="postion"\n'
        payload = payload + '\n'
        payload = payload + f'{XY[2]}|{XY[4]}\n'
        payload = payload + '--XXX--\n'
        headers = {
            'Referer': self.Referer,
            'sid': self.wps_sid,
            'User-Agent': self.UA,
            'Content-Type': 'multipart/form-data; boundary=XXX'
        }
        # print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        if j['result'] == 'ok':
            return True
        return False

    def SenSign(self):
        '''
        打卡
        :return:
        '''
        XY = ['38.5,44', '108.5,44', '178.5,44', '248.5,44', '318.5,44']
        captcha = parse.quote(f'{XY[2]}|{XY[4]}')
        url = f'https://zt.wps.cn/2018/clock_in/api/sign_up?formId=wechat&member=wps&client=wechat&_t={str(get_millisecond())}&client_code={self.client_code}&captcha={captcha}'
        payload = {}
        headers = {
            'sid': self.wps_sid,
            'Referer': self.Referer,
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        j = json.loads(response.text)
        if j['result'] == 'ok':
            return True
        return False

    def get_data(self):
        '''
        打卡排行榜
        :return:
        '''
        url = 'https://zt.wps.cn/2018/clock_in/api/get_data?member=wps'
        payload = {}
        headers = {
            # 'Host': 'zt.wps.cn',
            # 'Connection': 'keep-alive',
            'sid': self.wps_sid,
            'referer': self.Referer,
            # 'xweb_xhr': '1',
            'user-agent': self.UA,
            # 'Content-Type': 'application/json',
            # 'Accept': '*/*',
            # 'Sec-Fetch-Site': 'cross-site',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        j = json.loads(response.text)
        return j
