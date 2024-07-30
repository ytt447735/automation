import time
import ujson
from PIL import Image
from PIL import ImageEnhance
import requests
from io import BytesIO
from fun import baidu
import base64
from io import BytesIO


class wps:
    def __init__(self, cookie):
        self.Position = ["38%2C43", "105%2C50", "174%2C30", "245%2C50", "314%2C34"]  # 位置信息
        self.ck = cookie
        self.Referer = 'https://vip.wps.cn/spa/2021/wps-sign/?position=2020_vip_massing&client_pay_version=202301'
        self.Origin = 'https://vip.wps.cn'
        self.Log = ""

    # 获取奖励信息
    def get_reward(self):
        url = "https://personal-act.wps.cn/wps_clock/v2"

        headers = {
            'Origin': 'https://vip.wps.cn',
            'Cookie': self.ck
        }
        response = requests.request("GET", url, headers=headers)
        # print(response.text)
        j = ujson.loads(response.text)
        if j["result"] == "ok":
            self.Log = self.Log + "📝签到日志：\n"
            for i, element in enumerate(j["data"]["list"]):
                if element["status"] == 1:
                    status = "已领取"
                else:
                    status = "未领取"
                jj = ujson.loads(element["ext"])
                # print(jj[0])
                self.Log = self.Log + f"⌚️第{i + 1}天🎁奖励{jj[0]['hour']}小时会员🎊{status}\n"

    # 获取用户信息
    def get_check(self):
        url = "https://account.wps.cn/p/auth/check"

        payload = {}
        headers = {
            'Origin': 'https://vip.wps.cn',
            'Cookie': self.ck,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        j = ujson.loads(response.text)
        if j["result"] == "ok":
            self.Log = self.Log + f"👤用户信息：{j['nickname']}\n"
            return j['userid']
        self.Log = self.Log + f"👤用户信息：获取失败\n"
        return ""

    # 获取时间戳
    def get_time(self):
        return int(round(time.time() * 1000))

    # 处理验证码
    def code_processing(self):
        userid = self.get_check()
        if userid == "":
            return False
        url = f"https://personal-act.wps.cn/vas_risk_system/v1/captcha/image?service_id=wps_clock&t={self.get_time()}&request_id=wps_clock_{userid}"

        # 构造请求头，包含Cookie信息
        headers = {'Cookie': self.ck}

        # 发送带有Cookie的HTTP请求获取图片
        response = requests.get(url, headers=headers)
        img = response.content
        with open("code.png", 'wb') as f:
            f.write(img)
        img0 = Image.open(BytesIO(response.content))

        # img0 = Image.open('code.png')

        # 增强对比度
        enhancer = ImageEnhance.Contrast(img0)
        img = enhancer.enhance(2.0)

        # 水平分割图片成5张
        width, height = img.size
        segment_width = width // 5
        print(f"图片宽度: {width}, 分割后每张图片宽度: {segment_width}")

        segmented_images = []
        for i in range(5):
            left = i * segment_width
            right = (i + 1) * segment_width
            segment = img.crop((left, 0, right, height))
            segmented_images.append(segment)

        # 缓存分割后的图片
        # for i, segment_img in enumerate(segmented_images):
        #     output_buffer = BytesIO()
        #     segment_img.save(output_buffer, format='PNG')
        #     byte_data = output_buffer.getvalue()
        #     content = base64.b64encode(byte_data).decode("utf8")
        #     # print(content)
        #     # segment_img.save(f"segment_{i + 1}.png")

        P = ""
        L = "识别结果："
        # 对每张图片进行汉字识别
        for i, segment_img in enumerate(segmented_images):
            time.sleep(1.5)
            # text = pytesseract.image_to_string(segment_img, lang='chi_sim')
            # print(f"识别结果 {i+1}: {text}")
            output_buffer = BytesIO()
            segment_img.save(output_buffer, format='PNG')
            byte_data = output_buffer.getvalue()
            content = base64.b64encode(byte_data).decode("utf8")
            num = baidu.get_manage(content)
            # print(f"识别结果 {i + 1}: {num}")
            if num == 0:
                P = P + self.Position[i] + '%7C'
                L = L + f"{i + 1},"
        P = P.rstrip("%7C")
        L = L.rstrip(",") + "为倒立字"
        print(P)
        print(L)
        return self.submit_code(P)

    # 提交验证码
    def submit_code(self, c):
        url = "https://personal-act.wps.cn/wps_clock/v2"

        payload = {
            'double': '0',
            'v': '11.1.0.10314',
            'c': c
        }
        headers = {
            'Cookie': self.ck
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        j = ujson.loads(response.text)
        if j["result"] == "ok":
            self.Log = self.Log + f"今日签到成功，获得{j['data']['member']['hour']}小时会员\n"
            return True
        else:
            self.Log = self.Log + f"今日签到失败，{j['msg']}\n"
        return False

    # 签到兑换
    def exchange(self, day):
        url = f"https://vipapi.wps.cn/wps_clock/v2/exchange?day={day}"

        headers = {
            'Cookie': self.ck,
            'Origin': self.Origin,
            'Referer': self.Referer
        }

        response = requests.request("POST", url, headers=headers)
        print(response.text)
        j = ujson.loads(response.text)
        if j["result"] == "ok":
            self.Log = self.Log + f"兑换成功，获得{day}天会员\n"
            return True
        else:
            self.Log = self.Log + f"兑换失败，{j['msg']}\n"
            return False

    # 获取余额
    def get_balance(self):
        url = "https://vipapi.wps.cn/wps_clock/v2/user"

        payload = {}
        headers = {
            'Referer': self.Referer,
            'Origin': self.Origin,
            'Cookie': self.ck
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        j = ujson.loads(response.text)
        if j["result"] == "ok":
            total = j['data']['total'] // 3600
            cost = j['data']['cost'] // 3600
            self.Log = self.Log + f"🏦已使用额度：{ cost }小时({ cost // 24}天)\n"
            self.Log = self.Log + f"💰剩余额度：{total}小时({total // 24}天)\n"
            return j

    # 获取日志
    def get_log(self):
        return self.Log
