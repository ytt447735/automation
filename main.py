import os
from fun import wpspc
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
            for i in range(5):
                if w.code_processing():
                    print("第" + str(i + 1) + "次尝试签到成功")
                    break
                else:
                    print("第" + str(i + 1) + "次尝试签到失败")
            w.get_reward()  # 获取奖励信息
            w.get_balance()  # 获取余额
            # print("📝签到日志：")
            # print(w.get_log())
            notify.send("WPS_PC", w.get_log().replace('\n','\\n'))
        except Exception as e:
            print("出错了！详细错误👇错误CK👉" + mt_token)
            print(e)


if __name__ == '__main__':
    SenPC()
