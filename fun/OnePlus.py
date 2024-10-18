import ujson
import requests
import com
import re
import time

class oneplus:
    def __init__(self, cookie):
        self.ck = cookie
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
            print(f"activityId={self.activityId_activityInfo}")
        else:
            print("签到标识获取失败")
            self.Log = self.Log + f"📝签到失败，签到标识获取失败！\n"
        
        match = re.search(r'"taskActivityInfo":{"activityId":"(\d+)"', response.text)
        if match:
            self.activityId_taskActivityInfo = match.group(1)
            print(f"activityId={self.activityId_taskActivityInfo}")
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
                if taskStatus == 0:
                    if taskType == 0:
                        self.task_signInOrShareTask(taskName, taskId, activityId)
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
    def subscribes(self, skuId):
        url = "https://msec.opposhop.cn/goods/web/subscribes/goodsSubscribeV1"
        payload = f"type=1&skuId={ skuId }"
        headers = {
            'Cookie': self.ck,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.UA
        }
        response = requests.post(url, data=payload, headers=headers)
        print("subscribes",response.text)
        if j["code"] == 200:
            self.task_receiveAward()
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

                

