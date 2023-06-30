import requests
import json


class csdn:
    def __init__(self, UT, UN, XCaS, XCaSH, XCaN, XCaK):
        self.UT = UT
        self.UN = UN
        self.XCaS = XCaS
        self.XCaSH = XCaSH
        self.XCaN = XCaN
        self.XCaK = XCaK
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6919'
    def Getbyusername(self):
        """
        个人资料查询
        """
        cookies = {
            'UserName': self.UN,
            'UserToken': self.UT,
        }

        headers = {
            'X-Ca-Signature-Headers': self.XCaSH,
            # 'X-Ca-Signature': self.XCaS,
            # 'X-Ca-Nonce': self.XCaN,
            'X-Ca-Signature': 'qsh6ua6nN9jamuU+NTOPcnQZiaucAZYGIjaxXtHNES8=',
            'X-Ca-Nonce': '9b8b9ffd-bf06-4454-8b42-16857156fe5c',
            'X-Ca-Key': self.XCaK,
            'user-agent': self.UA,
            'referer': 'https://servicewechat.com/wx94ba57502711952f/110/page-frame.html',
            'Accept-Language': 'zh-CN,zh',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        data = {
            'username': self.UN,
        }
        response = requests.post(
            'https://miniapp-api.csdn.net/user-center/userinfo/getbyusername',
            json=data,
            cookies=cookies,
            headers=headers
        )
        # print(response.text)
        j = json.loads(response.text)
        R = ''
        if j['code'] == 200:
            R = '昵称：'+j['result']['nickname']+"\n"
        else:
            R = '昵称：未知' + "\n"
        return R

    def polymerize(self):
        """
        账户余额查询
        """
        cookies = {
            'UserName': self.UN,
            'UserToken': self.UT,
        }

        headers = {
            'X-Ca-Signature-Headers': self.XCaSH,
            'X-Ca-Signature': self.XCaS,
            'X-Ca-Nonce': self.XCaN,
            'X-Ca-Key': self.XCaK,
            'user-agent': self.UA,
            'referer': 'https://servicewechat.com/wx94ba57502711952f/110/page-frame.html',
            'Accept-Language': 'zh-CN,zh',
            'Content-Type': 'application/json',
        }
        params = {
            'startTime': '1686499200000',
            'endTime': '1686585600000',
            'profitType': '1',
        }
        response = requests.get(
            'https://miniapp-api.csdn.net/mall/mp/mallorder/api/internal/wallet/polymerize',
            params=params,
            cookies=cookies,
            headers=headers
        )
        # print(response.text)
        j = json.loads(response.text)
        R = ''
        if j['code'] == 200:
            R = "账户余额："+j['balance']['total']+ "\n"
        else:
            R = "账户余额：未知"+ "\n"
        return R