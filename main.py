#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: main.py(automation签到)
Author: ytt447735
cron: 8 0 * * *
new Env('automation签到');
Update: 2024/10/19
"""

import os
from fun import wpspc,OnePlus
import notify

def SenPC():
    wps_pc = os.getenv("wps_pc")
    if not wps_pc:
        notify.send("WPS_PC",'🙃wps PC CK 变量未设置')
        print('🙃wps PC CK 变量未设置')
        exit()
    wps_pc_list = wps_pc.split('&')
    print("-------------------总共" + str(int(len(wps_pc_list))) + "个wps_PC CK-------------------")
    for mt_token in wps_pc_list:
        try:
            w = wpspc.wps(mt_token)
            for i in range(6):
                if w.code_processing():
                    print("第" + str(i + 1) + "次尝试签到成功")
                    break
                else:
                    print("第" + str(i + 1) + "次尝试签到失败")
            w.get_reward()  # 获取奖励信息
            w.get_balance()  # 获取余额
            print("📝签到日志：")
            print(w.get_log())
            notify.send("WPS_PC", w.get_log().replace('\n','\\n'))
        except Exception as e:
            print("出错了！详细错误👇错误CK👉" + mt_token)
            print(e)

# OnePlus
def SenOnePlus():
    OnePlus_COOKIE = os.getenv("OnePlus_COOKIE")
    if not OnePlus_COOKIE:
        notify.send("OnePlus_COOKIE",'🙃OnePlus_COOKIE 变量未设置')
        print('🙃OnePlus_COOKIE 变量未设置')
        exit()
    ck_list = OnePlus_COOKIE.split('&')
    print("-------------------总共" + str(int(len(ck_list))) + "🙃OnePlus_COOKIE CK-------------------")
    for mt_token in ck_list:
        try:
            w = OnePlus.oneplus(mt_token)
            w.set_log("\n--------OPPO商城任务--------\n")
            t = w.get_activityId()
            w.shopping_signIn()
            w.get_task()
            w.membership_grade()
            w.integral_query()
            print(w.get_log())
            notify.send("OnePlus", w.get_log())
        except Exception as e:
            print("出错了！详细错误👇错误CK👉" + mt_token)
            print(e)
            notify.send("OnePlus", "出错了！详细错误👇错误CK👉" + mt_token +"\n错误内容:" + str(e))


if __name__ == '__main__':
    SenPC()
    SenOnePlus()
