#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: WPS签到
Author: youtantan
Date: 2023/6/13 18:59
cron: 0 9 * * *
new Env('WPS签到');
Update: 2023/6/14 优化信息输出效果
"""
import os
import time
from fun import wpswx
from fun import wpspc
from fun import pu
import notify

sen = ''
if_send = os.getenv("wps_send")

def SenWx():
    global sen
    senp=''
    wps_wx = os.getenv("wps_wx")
    if not wps_wx:
        sen='🙃wps 微信 CK 变量未设置\n'
        return
    wps_wx_list = wps_wx.split('&')
    senp=senp+'\n'+"-------------------总共" + str(int(len(wps_wx_list))) + "个wps_微信CK-------------------"
    for mt_token 在 wps_wx_list:
        ck = pu.convert_cookies_to_dict(mt_token)
        try:
            wx = wpswx.wps(ck["csrftoken"], ck["wps_sid"])
            Ch = wx.GetCheck()
            Da = None
            IsOK = False
            senp=senp+'\n'+f"👇👇👇在打卡中👇👇👇"
            for i 在 range(1， 20):
                wx.GetCode()
                time.sleep(0.5)
                if wx.SenSign():
                    time.sleep(0.5)
                    Da = wx.get_data()
                    IsOK = True
                    break
                time.sleep(1)
            senp=senp+'\n'+"昵称：" + Ch['nickname']
            if IsOK:
                senp=senp+'\n'+"打卡成功"
            else:
                senp=senp+'\n'+"打卡失败"
            senp=senp+'\n'+f"我成功打卡{str(Da['total_add_day'])}天"
            senp=senp+'\n'+f"今日共计{Da['pool_day']}人参与"
            senp=senp+'\n'+f"共计{Da['statistics']['success']}人成功，共计{Da['statistics']['fail']}人失败"
            senp=senp+'\n'+f'累计人{Da["total_sign_up"]}领取奖励'
            senp=senp+'\n'+f"👆👆👆打卡完毕👆👆👆\n"
        except Exception as e:
            senp=senp+'\n'+"出错了！详细错误👇错误CK👉" + mt_token
            senp=senp+'\n'+str(e)
        print(senp)
        sen=sen+senp


def SenPC():
    global sen
    senp = ''
    wps_pc = os.getenv("wps_pc")
    if not wps_pc:
        sen='🙃wps PC CK 变量未设置\n'
        return
    wps_pc_list = wps_pc.split('&')
    senp=senp+'\n'+"-------------------总共" + str(int(len(wps_pc_list))) + "个wps_PC CK-------------------"
    for mt_token 在 wps_pc_list:
        ck = pu.convert_cookies_to_dict(mt_token)
        try:
            pc = wpspc.wps(ck["wpsua"], ck["wps_sid"])
            Ch = pc.GetCheck()
            senp=senp+'\n'+f"👇👇👇在打卡中👇👇👇"
            senp=senp+'\n'+"🎁开始👉会员时效签到👇"
            senp=senp+'\n'+"昵称：" + Ch['nickname']
            if pc.Signin():
                senp=senp+'\n'+"打卡成功"
            else:
                senp=senp+'\n'+"打卡失败"
            Q = pc.GetQuota() // 3600
            senp=senp+'\n'+pc.Index()
            senp=senp+'\n'+f"当前时间额度为{str(Q)}小时({Q//24}天)"
            senp=senp+'\n'+"🎁开始👉空间签到👇"
            if pc.SenSpace():
                senp=senp+'\n'+"签到成功"
            else:
                senp=senp+'\n'+"签到失败"
            senp=senp+'\n'+pc.GetSpace()
            if 'day' 在 mt_token:
                d=ck['day']
                if pc.SenExchange(d):
                    senp = senp + '\n' + f"兑换{d}天成功"
                else:
                    senp = senp + '\n' + f"兑换{d}天失败"

            if pc.DocerSign():
                senp = senp + '\n' + f"稻壳PPT签到成功"
            else:
                senp = senp + '\n' + f"稻壳PPT签到失败"

            senp=senp+'\n'+f"👆👆👆打卡完毕👆👆👆\n"
        except Exception as e:
            senp=senp+'\n'+"出错了！详细错误👇错误CK👉" + mt_token
            senp=senp+'\n'+str(e)
        print(senp)
        sen=sen+senp


if __name__ == '__main__':
    SenWx()
    SenPC()
    if if_send == 'true':
        notify.send('WPS打卡',sen)
