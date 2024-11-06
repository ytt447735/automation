#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: OnePlus.py(OnePlus签到)
Author: ytt447735
cron: 0 8 * * *
new Env('OnePlus签到');
Update: 2024/10/19
"""
import os,notify
import ujson
import requests
import re
import time
from fun import com

class oneplus:
    def __init__(self):
        self.ck = ''
        self.Log = ""
        self.UA = "Mozilla/5.0 (Linux; Android 14; LE2120 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 oppostore/403201 ColorOS/V14.0.0 brand/OnePlus model/LE2120;kyc/h5face;kyc/2.0;netType:NETWORK_WIFI;appVersion:403201;packageName:com.oppo.store"
        self.activityId_activityInfo = ""
        self.activityId_taskActivityInfo = ""

    # 获取签到标识
    def get_activityId(self):
        url = "https://hd.opposhop.cn/bp/b371ce270f7509f0?nightModelEnable=true&us=wode&um=qiandaobanner"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        # "activityInfo":{"activityId":"1838147945355288576",
        # "taskActivityInfo":{"activityId":"1838149802563739648",
        match = re.search(r'"activityInfo":{"activityId":"(\d+)"', response.text)
        if match:
            # return self.shopping_signIn(match.group(1))
            self.activityId_activityInfo = match.group(1)
            print(f"activactivityId_activityInfoityId={self.activityId_activityInfo}")
        else:
            print("签到标识获取失败")
            self.Log = self.Log + f"📝签到失败，签到标识获取失败！\n"
        
        match = re.search(r'"taskActivityInfo":{"activityId":"(\d+)"', response.text)
        if match:
            self.activityId_taskActivityInfo = match.group(1)
            print(f"activityId_taskActivityInfo={self.activityId_taskActivityInfo}")
        else:
            print("任务标识获取失败")
            self.Log = self.Log + f"📝签到失败，任务标识获取失败！\n"



    # 商城签到
    def shopping_signIn(self):
        if self.activityId_activityInfo =="":
            return
        url = "https://hd.opposhop.cn/api/cn/oapi/marketing/cumulativeSignIn/signIn"
        payload = ujson.dumps({
        "activityId": self.activityId_activityInfo
        })
        headers = {
            'Cookie': self.ck,
            'User-Agent': self.UA,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print("shopping_signIn",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            awardType = j['data']['awardType']
            awardValue = j['data']['awardType']
            if awardType == 1:
                self.Log = self.Log + f"📝签到成功，奖励{ awardValue } 积分\n"
        else:
            message = j['message']
            self.Log = self.Log + f"📝签到失败，{ message }\n"
    

    # 积分额度查询
    def integral_query(self):
        url = "https://msec.opposhop.cn/users/web/memberCenter/assets?couponStatus=1&couponType=0"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("integral_query",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            self.Log = self.Log + "💰当前余额：\n"
            for i, element in enumerate(j["data"]): 
                title = element["title"]
                text = element["text"]
                Type = element["type"]
                if Type == "coupon" or Type == "credit" or Type == "growing":
                    self.Log = self.Log + f"👛{ title }：{ text }\n"
            

    # 会员等级
    def membership_grade(self):
        url = "https://msec.opposhop.cn/users/web/memberCenter/getMemberExpDetail"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("membership_grade",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            gradeName = j['data']['gradeName']
            des = j['data']['des']
            self.Log = self.Log + f"🎖️会员等级：{ gradeName }({ des })\n"


    # 获取任务列表
    def get_task(self):
        if self.activityId_taskActivityInfo=="":
            return
        url = f"https://hd.opposhop.cn/api/cn/oapi/marketing/task/queryTaskList?activityId={ self.activityId_taskActivityInfo }&source=c"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("get_task",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            for i, element in enumerate(j["data"]["taskDTOList"]):
                taskName = element['taskName']
                taskId = element['taskId']
                activityId = element['activityId']
                taskType = element['taskType'] # 1=浏览，4=预约， 6=开卡/购买
                taskStatus = element['taskStatus'] # 是否完成
                attachConfigTwo_link = element['attachConfigTwo']['link']
                skuId = ''
                match = re.search(r'skuId=(\d+)', attachConfigTwo_link)
                if match:
                    skuId = match.group(1)


                tt = self.button_text_status(element)
                if tt == 2:
                    self.task_signInOrShareTask(taskName, taskId, activityId)
                elif tt==3:
                    print(f"skuId={skuId}")
                    self.subscribes(skuId,taskName, taskId, activityId)
                else:
                    self.Log = self.Log + f"❌{ taskName } 任务执行失败，{ tt }\n"
                time.sleep(3)

    # 提交任务
    def task_signInOrShareTask(self, taskName, taskId, activityId):
        url = f"https://hd.opposhop.cn/api/cn/oapi/marketing/taskReport/signInOrShareTask?taskId={ taskId }&activityId={ activityId }&taskType=1"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("task_signInOrShareTask",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            self.task_receiveAward(taskName, taskId, activityId)
        else:
            message = j['message']
            self.Log = self.Log + f"❌{ taskName } 任务提交失败，{ message }\n"
            

    
    # 领取任务奖励
    def task_receiveAward(self, taskName, taskId, activityId):
        url = f"https://hd.opposhop.cn/api/cn/oapi/marketing/task/receiveAward?taskId={ taskId }&activityId={ activityId }"
        payload = {}
        headers = {
            'Cookie': self.ck,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.UA
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print("task_receiveAward",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            awardType = j['data']['awardType']
            awardValue = j['data']['awardType']
            if awardType == 1:
                self.Log = self.Log + f"✅{taskName} 任务完成，奖励{ awardValue } 积分\n"
        else:
            message = j['message']
            self.Log = self.Log + f"❌{ taskName } 任务失败，{ message }\n"

    # 预约任务
    def subscribes(self, skuId,taskName, taskId, activityId):
        url = "https://msec.opposhop.cn/goods/web/subscribes/goodsSubscribeV1"
        payload = f"type=1&skuId={ skuId }"
        headers = {
            'Cookie': self.ck,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/4.9.3.6'
        }
        response = requests.post(url, data=payload, headers=headers)
        # response = requests.request("POST", url, headers=headers, data=payload)
        print("subscribes",response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            self.task_receiveAward(taskName, taskId, activityId)
        else:
            message = j['errorMessage']
            self.Log = self.Log + f"❌{ taskName } 预约失败，{ message }\n"

    # 新增日志
    def set_log(self,text):
        self.Log = self.Log + text


    # 获取日志
    def get_log(self):
        # return self.Log.replace("\n","\r\n")
        return self.Log



    def button_text_status(self,t):
        TASK_STATUS = {
            'PREPARE_FINISH': 1,
            'GO_AWARD': 2,
            'FINISHED': 3,
            'NOT_REMAINING_NUMBER': 6
        }
        task_type_texts = [
            1,# "立即签到",
            2,# "去看看",
            4,# "去分享",
            2,# "去逛逛",
            3,# "去预约",
            3,# "去预约",
            3,# "去预约",
            5,# "去购买",
            6,# "去组队",
            2,# "去看看",
            3,# "去预约",
            7,# "去完成",
            8,# "去添加",
            9,# "去认证",
            10,# "去关注",
            11,# "去填写",
            2,# "去逛逛",
            2,# "去看看"
        ]

        if t['taskStatus'] == TASK_STATUS['PREPARE_FINISH']:
            # return task_type_texts.get(t['taskType'], "已结束")
            return task_type_texts[t['taskType']]
        elif t['taskStatus'] == TASK_STATUS['GO_AWARD']:
            return "领奖励"
        elif t['taskStatus'] == TASK_STATUS['NOT_REMAINING_NUMBER']:
            return "领光了"
        elif t['taskStatus'] == TASK_STATUS['FINISHED']:
            return "已完成"
        else:
            return "已结束"
    

    # 钱包签到
    def continueSign(self):
        url = "https://hwallet.finzfin.com/act/usersign/v1/continueSign"

        payload = ujson.dumps({
        "actId": "AID202207111442220933",
        "funcId": "CONTINUEV2202209161649037309"
        })

        headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 14; LE2120 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36;webank/h5face;webank/2.0 JSBridge/1 wallet/5.31.0_befb176_240927 FinshellWebSDK/3.0.2.74",
        'Accept': "application/json;charset=UTF-8",
        'Content-Type': "application/json",
        'x-token': "TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE3MzE4Mzc3NzYyMTgsImlkIjoiNjk5ODkzMDU5IiwiaWRjIjoic2hvdW1pbmciLCJ0aWQiOiJYR2VCNUN4SkRyM25MN0lna2R5aHZ0RlFIczNWdXF1d3hNdTNBWFM4UGZPMHdwcXh0WmtXTkVWWGJ0cTJNTEZOS1dYK2Rpa0xmakZnZ2luNEtxK0JpZm0rTEdVeUtJNWdvUDlqbG9RVlpmST0ifQ.MEUCIQDTYNCBx3iliVXlR79AUkyZdPRfoCzePXtw2mY2eDIyuAIgF6hirnqnJunzzQpr1yq86QLQEWwaPGXOIlPV_GU6UBo"
        }

        response = requests.post(url, data=payload, headers=headers)
        # response = requests.request("POST", url, headers=headers, data=payload)
        print("continueSign", response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            print(1)
        else:
            message = j['msg']
            self.Log = self.Log + f"❌签到失败，{ message }\n"


     # 一加论坛签到
    def bbsSign(self):
        url = "https://bbs-api-cn.oneplus.com/task/api/sign/v1/create"
        params = {
        'ver': "bbs42703",
        'timestamp': com.get_time(),
        # 'sign': ""
        }
        headers = {
        'User-Agent': "bbs/android/42703",
        'Accept-Encoding': "gzip",
        'model': "LE2120",
        'osver': "android14",
        'romv': "LE2120_14.0.0.720(CN01)",
        'lang': "zh-CN",
        'token': com.GetIntermediateText(self.ck,"TOKENSID=",";"),
        'tz': "Asia/Shanghai"
        }
        response = requests.post(url, params=params, headers=headers)
        print(response.text)
        j = ujson.loads(response.text)
        if j["code"] == 200:
            if j['data']['todaySigned']==True:
                self.Log = self.Log +'今天已经签到过啦！\n'
            else:
                self.Log = self.Log +'今天签到成功！\n'
            self.Log = self.Log + '累计签到：'+str(j['data']['signDays'])+'天\n'
            self.Log = self.Log + '连续签到：'+str(j['data']['continuousSignDays'])+'天\n'
            self.Log = self.Log + '再连续签到'+str(j['data']['extSignDays'])+'天，可额外获得'+str(j['data']['extCredit'])+'积分\n'
        else:
            self.Log = self.Log +"一加论坛签到失败，"+j['msg']+"\n"


    def run(self):
        OnePlus_COOKIE = os.getenv("OnePlus_COOKIE")
        if not OnePlus_COOKIE:
            notify.send("OnePlus_COOKIE",'🙃OnePlus_COOKIE 变量未设置')
            print('🙃OnePlus_COOKIE 变量未设置')
            exit()
        ck_list = OnePlus_COOKIE.split('&')
        print("-------------------总共" + str(int(len(ck_list))) + "🙃OnePlus_COOKIE CK-------------------")
        for mt_token in ck_list:
            try:
                self.ck = mt_token
                self.set_log("\n--------一加论坛签到--------\n")
                r.bbsSign()
                self.set_log("\n--------OPPO商城任务--------\n")
                t = self.get_activityId()
                self.shopping_signIn()
                self.get_task()
                self.membership_grade()
                self.integral_query()
                # self.continueSign()
                print(self.get_log())
                notify.send("OnePlus", self.get_log())
            except Exception as e:
                print("出错了！详细错误👇错误CK👉" + mt_token)
                print(e)
                notify.send("OnePlus", "出错了！详细错误👇错误CK👉" + mt_token +"\n错误内容:" + str(e))


if __name__ == '__main__':
    r = oneplus()
    r.run()
