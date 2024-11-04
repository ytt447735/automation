#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: SunLogin.py(贝锐签到)
Author: ytt447735
cron: 2 8 * * *
new Env('贝锐签到');
Update: 2024/10/19
"""
import ujson
import requests
import base64
import hashlib
import time
import os
import notify

class sunlogin:
    def __init__(self):
        self.ck = ''
        self.Log = ""


    # 阳光小店-每日签到
    def income(self):
        url = "https://store-api.oray.com/point/1/income"
        headers = {
        'User-Agent': "SLCC/15.3.1.66811 (Android)",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        'Cookie': self.ck
        }
        response = requests.post(url, headers=headers)
        print(response.text)
        if "code" in response.text:
            j = ujson.loads(response.text)
            self.Log = self.Log + j['message'] +'\n'
            return
        if "userid" in response.text:
            j = ujson.loads(response.text)
            self.Log = self.Log + "签到成功，获得🌞" + str(j['pointtotal']) + '阳光值\n'
            return
        self.Log = self.Log + "签到失败，未知错误\n"


    def sign(self):
        url = "https://store-api.oray.com/points/sign"
        headers = {
        'User-Agent': "SLCC/15.3.1.66811 (Android)",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        'Cookie': self.ck
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        if '签到成功' in response.text:
            j = ujson.loads(response.text)
            self.Log = self.Log + j['arguments']['dialogtitle'] + j['arguments']['dialogdesc']+"\n"
        else:
            self.Log = self.Log + "签到失败"+"\n"


    #收集阳光
    def production(self, pointdailyid):
        url = f"https://store-api.oray.com/points/{pointdailyid}/daily"
        headers = {
        'User-Agent': "SLCC/15.3.1.66811 (Android)",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': self.ck
        }
        response = requests.post(url, headers=headers)
        print(response.text)
        if "code" in response.text:
            j = ujson.loads(response.text)
            self.Log = self.Log +j["message"]+"\n"
        else:
            self.Log = self.Log + "☀️x1 收集成功\n"

    
    # 获取阳光列表
    def getDailys(self):
        url = f"https://store-api.oray.com/points/daily"
        headers = {
        # 'User-Agent': "SLCC/15.3.1.66811 (Android)",
        # 'Accept': "application/json, text/plain, */*",
        # 'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        # 'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': self.ck
        }
        response = requests.get(url, headers=headers)
        print("getDailys:"+response.text + '🔚')
        j = ujson.loads(response.text)
        for i, element in enumerate(j):
            id = element['pointdailyid']
            userid = element['userid']
            print(id)
            self.production(id)
            time.sleep(2)

    # 获取阳光余额
    def getPlants(self):
        url = "https://store-api.oray.com/point/plants"
        headers = {
        # 'User-Agent': "SLCC/15.3.1.66811 (Android)",
        # 'Accept': "application/json, text/plain, */*",
        # 'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        # 'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': self.ck
        }
        response = requests.get(url, headers=headers)
        print("getPlants:"+response.text)
        if '' == response.text:
            return False
        j = ujson.loads(response.text)
        if "pointtotal" in response.text:
            self.Log = self.Log +"☀️余额："+str(j['pointtotal'])+"\n"
            return True
        else:
            self.Log = self.Log +"☀️余额：未知\n"
        return False
            
    # 提交任务
    def setIncome(self,key):
        url = "https://store-api.oray.com/point/0/income"
        k = key.replace('=','%3D')
        payload = f"point_key={k}"
        headers = {
        # 'User-Agent': "SLCC/15.3.1.66811 (Android)",
        # 'Accept': "application/json, text/plain, */*",
        # 'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        # 'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': self.ck
        }
        response = requests.post(url, data=payload, headers=headers)
        print("setIncome:"+response.text)
        message = ''
        if 'userid' in response.text:
            return True, message
        if 'message' in response.text:
            j = ujson.loads(response.text)
            message = j['message']
        return False, message


    # 获取任务列表
    def getPoints(self,brand):
        url = f'https://store-api.oray.com/points?brand={brand}'
        headers = {
        # 'User-Agent': "SLCC/15.3.1.66811 (Android)",
        # 'Accept': "application/json, text/plain, */*",
        # 'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Referer': "https://sunlight.oray.com/",
        # 'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': self.ck
        }
        response = requests.get(url, headers=headers)
        print("getDailys:"+response.text)
        j = ujson.loads(response.text)
        for i, element in enumerate(j):
            name = element['name']
            count = element['condition']['count']
            used = element['used']
            print(count,used)
            if used == count:
                self.Log = self.Log + name +f"({str(count)}/{str(count)})  ✅已完成\n"
                continue
            acc = used
            for i in range(count-used):
                pointid = element['pointid']
                print(pointid,count,used)
                pointid = self.pointjm(str(pointid))
                message = ''
                isOK, message = self.setIncome(pointid)
                if isOK:
                    acc = acc + 1
                    message = '✅已完成'
                else:
                    message = "❌失败，"+message
                time.sleep(10)
                # break
            self.Log = self.Log + name +f"({str(acc)}/{str(count)})  {message}\n"
            time.sleep(3)
            # break
            

    # 加密
    def pointjm(self, t):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        key = "Nx4xnfHmGzz4t1rH"
        l = hashlib.md5(key.encode()).hexdigest()
        c = l[:16]
        d = l.encode('utf-8')
        h = c.encode('utf-8')
        cipher = AES.new(d, AES.MODE_CBC, h)
        e = t.encode('utf-8')
        n = cipher.encrypt(pad(e, AES.block_size))
        return base64.b64encode(n).decode('utf-8')
        # Example usage
        # t = "3"
        # result = encrypt(t)
        # print(result)  # Output should be "flEnHDBJMbe1mlNaEFKtzw=="

        # flEnHDBJMbe1mlNaEFKtzw==


    # 新增日志
    def set_log(self,text):
        self.Log = self.Log + text


    # 获取日志
    def get_log(self):
        # return self.Log.replace("\n","\r\n")
        return self.Log
    
    # 执行
    def run(self):
        task_name = '贝锐'
        ck_value = 'BR_COOKIE'
        CKS = os.getenv(ck_value)
        if not CKS:
            notify.send(task_name,f'🙃{ck_value} 变量未设置')
            print(f'🙃{ck_value} 变量未设置')
            exit()
        CKS_list = CKS.split('&')
        print("-------------------总共" + str(int(len(CKS_list))) + f"个{ck_value} CK-------------------")
        for mt_token in CKS_list:
            # try:
            self.ck = mt_token
            if self.getPlants() == False:
                self.set_log('⚠️ '+mt_token+ '  CK失效了')
                continue
            self.set_log("\n--------阳光小店签到--------\n")
            self.income()
            self.getDailys() # 收集阳光
            self.set_log("\n--------阳光任务--------\n")
            self.getPoints(3)
            self.getPoints(2)
            self.getPoints(0)
            self.getPlants() #最终额度
            # except Exception as e:
            #     print("出错了！详细错误👇错误CK👉" + mt_token)
            #     print(e)
            #     notify.send(task_name, "出错了！详细错误👇错误CK👉" + mt_token +"\n错误内容:" + str(e))
        print(self.get_log())
        notify.send(task_name, self.get_log())


if __name__ == '__main__':
    w = sunlogin()
    w.run()