import time

import requests
import json
from fun.pu import get_millisecondToTim
from fun.pu import get_millisecond


class wps:
    def __init__(self, wpsua, wps_sid):
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.20 Safari/537.36'
        self.Referer = 'https://vip.wps.cn/spa/2021/wps-sign/?position=2020_vip_massing&client_pay_version=202301'
        self.Origin = 'https://vip.wps.cn'
        self.p = 'EHkk0AYnPraZs9%2FxHs77MawspohSbN%2B3oM8CIvAs%2BNAc%2FYlFBN3KXKhNmLrEe%2BCWw6XnMEpoy3RQJJrDf%2FUxCm7p95EckQCkwjqxwjNAy2oMzwCoq%2B7HzvZUi%2FvmQl0%2F6lqvriaJzUeMzHjpJwj2EcPUSeQMDulTNFrEmnOACvc%3D'
        self.v = '11.1.0.14036'
        self.wpsua = wpsua
        self.wps_sid = wps_sid

    def Signin(self):
        '''
        签到
        :return:
        '''
        url = f"https://vipapi.wps.cn/wps_clock/v2?double=0&p={self.p}&v={self.v}"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        j = json.loads(response.text)
        if j["result"] == "ok":
            return True
        else:
            print('打卡失败，延迟30秒继续')
            time.sleep(60)
            return self.Signin()
        # {"data":{},"msg":"RecordTimeOut","result":"error"}
        # return False

    def GetCheck(self):
        """
        个人资料
        :return:
        """
        url = "https://account.wps.cn/p/auth/check"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'User-Agent': self.UA,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        if j["result"] == "ok":
            return j
        return None

    def GetQuota(self):
        """
        额度查询
        :return:
        """
        url = "https://vipapi.wps.cn/wps_clock/v2/user"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        if j["result"] == "ok":
            return j["data"]["total"]
        return 0

    def Index(self):
        """
        签到查询
        :return:
        """
        url = "https://vipapi.wps.cn/wps_clock/v2"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        # print(j)
        endtime = get_millisecondToTim(j['data']['end'])
        starttime = get_millisecondToTim(j['data']['start'])
        R = f"签到周期：{endtime}至{starttime}"
        for v in j['data']["list"]:
            # print(v['status'],v['times'],json.loads(v['ext'])[0]['hour'])
            if v['status'] == 1:
                R = R + '\n' + f"第{str(v['times'])}天奖励{str(json.loads(v['ext'])[0]['hour'])}小时，签到成功"
            else:
                R = R + '\n' + f"第{str(v['times'])}天奖励{str(json.loads(v['ext'])[0]['hour'])}小时，未签到"
        print(R)
        return R

    def SenExchange(self, day):
        """
        签到兑换vip天数
        :return:
        """
        url = "https://vipapi.wps.cn/wps_clock/v2/exchange"
        payload = f'day={day}'
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        if j['result'] == 'ok':
            return True
        return False

    def GetSpace(self):
        """
        空间查询
        :return:
        """
        url = "https://vip.wps.cn/sign/mobile/v3/get_data"
        payload = {}
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        # print(j['data']['integral'])
        R = "积分：" + str(j['data']['integral'])
        R = R + '\n' + "空间：" + str(j['data']['spaces_info']['used']) + "/" + str(
            j['data']['spaces_info']['total']) + str(j['data']['spaces_info']['unit'])
        for inx, val in enumerate(j['data']["reward_list"]['space']['normal']):
            # print(inx,val)
            if j['data']["history"]['data'][inx]['type'] == 1:
                R = R + '\n' + f"第{str(inx + 1)}天{str(val)}M(会员加{str(j['data']['reward_list']['space']['member'][inx])}M)，签到成功"
            else:
                R = R + '\n' + f"第{str(inx + 1)}天{str(val)}M(会员加{str(j['data']['reward_list']['space']['member'][inx])}M)，未签到"
        print(R)
        return R

    def SenSpace(self):
        """
        空间签到
        :return:
        """
        url = "https://vip.wps.cn/sign/v2"
        payload = 'platform=8'
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        j = json.loads(response.text)
        # print(j)
        # {'result': 'error', 'data': '', 'msg': 'need_captcha'}
        # print(j['result']+j['msg'])
        if j["result"] == "ok":
            return True
        if j["result"] == "error":
            if j["msg"] == "need_captcha":  # 需验证码
                # for i in range(30):
                #     self.GetSpaceCode()
                #     time.sleep(0.2)
                #     if self.SenSpaceCode():
                #         break
                #     time.sleep(3)
                print('需要验证码')

        return False

    def GetSpaceCode(self):
        """
        空间验证码获取
        :return:
        """
        url = "https://vip.wps.cn/checkcode/signin/captcha.png?platform=8&encode=0&img_witdh=336&img_height=84.48&v=" + str(
            get_millisecond())
        headers = {
            'Referer': 'https://zt.wps.cn/spa/2019/vip_mobile_sign_v2/?csource=pc_cloud_personalpanel&position=pc_cloud_sign',
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        r = requests.get(url, headers=headers)

    def SenSpaceCode(self):
        """
        空间验证码提交
        :return:
        """
        url = "https://vip.wps.cn/sign/v2"
        headers = {
            'Referer': 'https://zt.wps.cn/spa/2019/vip_mobile_sign_v2/?csource=pc_cloud_personalpanel&position=pc_cloud_sign',
            'Origin': self.Origin,
            'Cookie': f'wpsua={self.wpsua};wps_sid={self.wps_sid}',
            'User-Agent': self.UA
        }
        payload = 'platform=8&captcha_pos=152.0125%2C25.0125&img_witdh=336&img_height=85'
        params = {
            'platform': '8',
            'captcha_pos': '152.0125%2C25.0125',
            'img_witdh': '336',
            'img_height': '85'
        }
        # response = requests.request("POST", url, headers=headers, data=payload)
        response = requests.post(url, params, headers=headers)
        print(response.text)
        j = json.loads(response.text)
        # {"result":"error","data":"","msg":"captcha_not_match"}
        if j['result'] == 'error':
            return False
        return True

    def DocerSign(self):
        """
        WPS稻壳ppt小程序签到➡领取PPT
        :return:
        """
        url = "https://welfare.docer.wps.cn/sign_in/v1/user_sign_in"
        payload = "{}"
        headers = {
            'Referer': 'https://servicewechat.com/wxdf769165d0c9f6bc/122/page-frame.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6919',
            'Cookie': f'wps_sid={self.wps_sid}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        j = json.loads(response.text)
        if j['data'] == 'ok':
            return True
        return False
