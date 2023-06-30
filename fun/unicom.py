import requests
import json

class unicom:

    def SigninApp(self):
        cookies = {
            # 'SigninApp': 'd2a1b227ea5520dac49e79554f3247d0',
            # 'MUT_S': 'android13',
            # 'devicedId': '367afdb83b234e64be138dcc2826938d',
            # 'login_type': '01',
            # 'u_account': '17606537727',
            # 'city': '036|360|90063345|-99',
            # 'd_deviceCode': '95daa06b8e30439b83d237fd53795251',
            # 'random_login': '0',
            # 'c_mobile': '17606537727',
            # 'wo_family': '0',
            # 'u_areaCode': '',
            # 'cdn_area': '36|360',
            # 'c_version': 'android@10.0500',
            # 'cw_mutual': '6ff66a046d4cb9a67af6f2af5f74c3211681e909aa79a35a82f32c364a383e18792a8eb02866bde01520ca2a6328d40578216e7a2dd1b2c9f3dfbb9cf60e9ff7',
            # 'clientid': '98|0',
            # 'REQ_FLAG': '2',
            # 'TOTAL_PAGES': '2',
            # 'PvSessionId': '20230609203106cbf00c28e9ee4bdeb9e96f536202a9e7',
            # 'unicomMallUid': '17606537727',
            # '_jf_id': 'ggtdwaomde91b100d264ef3e9dc1e7a1ecd97d4bygx8mvve',
            # 'jfcity': '36|360',
            # 'jfuser_id': '7516110115948768',
            # 'jfuser': '01|2002|99|17606537727',
            # 'a_token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY5MTg5MDQsInRva2VuIjp7ImxvZ2luVXNlciI6IjE3NjA2NTM3NzI3IiwicmFuZG9tU3RyIjoieWgxY2MxYTIxNjg2MzE0MTA0In0sImlhdCI6MTY4NjMxNDEwNH0.4c8ZzsyqHwa1vQHxMF4r9S6mKcxriyWgA95VR30YnTy7czU9xYx5uTgk9k8ZJYg3JDI9B16-U60rd-7IET0Oow',
            # 'c_id': '294e6b399cf5382a2e55a77b04f9eb913f8e2989c14a6fdd2fbddb742bab7fd0',
            # 'enc_acc': 'RJfg6sQli8EEexpsPxgoijf3wa9vmllVIBxwsoPA76XUVqIGQlJ+KiddBO8Y1AlbjW6CvFQ2ZIXuUf9Eb1mHLLSjotS4DRDWQ21Ad2Yo5wm6+c7J2/nrCFzmshNT5YAk6T3hJ2auOq1HKgZc8P7Qzkp+ITFg2iBU1YW5ODwusAM=',
            # 'ecs_acc': 'RJfg6sQli8EEexpsPxgoijf3wa9vmllVIBxwsoPA76XUVqIGQlJ+KiddBO8Y1AlbjW6CvFQ2ZIXuUf9Eb1mHLLSjotS4DRDWQ21Ad2Yo5wm6+c7J2/nrCFzmshNT5YAk6T3hJ2auOq1HKgZc8P7Qzkp+ITFg2iBU1YW5ODwusAM=',
            # 't3_token': '5e399e715ccd5da3fda21a021215e7ba',
            # 'invalid_at': 'fd958f87db9723b87333b34556099a99e13f004576d8a063f385fb44787e4a3d',
            # 'third_token': 'eyJkYXRhIjoiMTMyYzJlNGFmOTFiOWU0ZTRmMmMyMDQwOWVkNWU5NDI2Y2Q0MmM3NDYxZjI1NzgzNTJmYTYwMmM1ZTA3NTBlODMwMzI5YzgyOTJiY2Q0ZmQ2N2I4OTllNTI5NzI3ZDlhYTM5OGViMWVhZGE1MWVmNzkzODViMDAzNWM2MDBlYzc0M2U0ZDIyMmQ1MjM0YzMxMDliMjBjZTAwZmZlNTc2NSIsInZlcnNpb24iOiIwMCJ9',
            'ecs_token': 'eyJkYXRhIjoiMjA0ZWM1NDcwMThkMjFlOWMyYzRmMzBhNjc5YzZhMTA5ODc5ODJmOGNiZWU1NTJjYjZlMDYzOWZhNTBmZGM1MjE3ZDFkZDBjMTdlOGRmM2UwMzg4YTg3NDA5MDYzMzRmMTQ3NjhlYTJhM2NlODQ5YWJhN2IxODA2MzYxZjdiNzE3M2M3NWZlYTQ1ZTg2NGQ2ZWI0MjFjYjk0YzExYmZkMDdhNmJkNDgwMWVlN2NiNWIyYjE3NTc1ODcwMmUzMTdhOGI4YTkxY2VkNzIxNjRlZmJmYTk2ZTM3ODk4MmUxYTZlYmJlNTYzODVkOTM2MDRjZTkyYmM5N2Q1ZTAwMTkxM2Q3ZDYyMWM2MWYwNzg1Y2EwYWFkNzY0MGQ3ZDhlZDdhZDBhZGIwYmZkYTUyMzMzYmY2NzQzOTYwZWJlM2I1MWZhODhjNzc5YWM1ZDIyZmM1NDdjMzQ4ODJjMGQ4ZGIwMiIsInZlcnNpb24iOiIwMCJ9',
            # 'jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIxNzYwNjUzNzcyNyIsInBybyI6IjAzNiIsImNpdHkiOiIzNjAiLCJpZCI6ImNhZTE4ZDcyNTI1MjcxNDM4YjQxY2MwOWQwNzBmNDUyIn0.6iX9wQuCqCfh6y2G0ATHIjsLS0zyA-cbFkiiUwVJh0M',
            # 'SHAREJSESSIONID': '119812BBC4825E9FE1B64452BB432987',
            # 'acw_tc': '7ae4439c16863141700762552e6c21c84271e1441023473ff420388af9',
        }

        headers = {
            # 'Host': 'act.10010.com',
            # 'content-length': '19',
            # 'pragma': 'no-cache',
            # 'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; LE2120 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36; unicom{version:android@10.0500,desmobile:17606537727};devicetype{deviceBrand:OnePlus,deviceModel:LE2120};{yw_code:}',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://img.client.10010.com',
            # 'x-requested-with': 'com.sinovatech.unicom.ui',
            # 'sec-fetch-site': 'same-site',
            # 'sec-fetch-mode': 'cors',
            # 'sec-fetch-dest': 'empty',
            'referer': 'https://img.client.10010.com/',
            # 'accept-encoding': 'gzip, deflate',
            # 'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': 'SigninApp=d2a1b227ea5520dac49e79554f3247d0; MUT_S=android13; devicedId=367afdb83b234e64be138dcc2826938d; login_type=01; u_account=17606537727; city=036|360|90063345|-99; d_deviceCode=95daa06b8e30439b83d237fd53795251; random_login=0; c_mobile=17606537727; wo_family=0; u_areaCode=; cdn_area=36|360; c_version=android@10.0500; cw_mutual=6ff66a046d4cb9a67af6f2af5f74c3211681e909aa79a35a82f32c364a383e18792a8eb02866bde01520ca2a6328d40578216e7a2dd1b2c9f3dfbb9cf60e9ff7; clientid=98|0; REQ_FLAG=2; TOTAL_PAGES=2; PvSessionId=20230609203106cbf00c28e9ee4bdeb9e96f536202a9e7; unicomMallUid=17606537727; _jf_id=ggtdwaomde91b100d264ef3e9dc1e7a1ecd97d4bygx8mvve; jfcity=36|360; jfuser_id=7516110115948768; jfuser=01|2002|99|17606537727; a_token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY5MTg5MDQsInRva2VuIjp7ImxvZ2luVXNlciI6IjE3NjA2NTM3NzI3IiwicmFuZG9tU3RyIjoieWgxY2MxYTIxNjg2MzE0MTA0In0sImlhdCI6MTY4NjMxNDEwNH0.4c8ZzsyqHwa1vQHxMF4r9S6mKcxriyWgA95VR30YnTy7czU9xYx5uTgk9k8ZJYg3JDI9B16-U60rd-7IET0Oow; c_id=294e6b399cf5382a2e55a77b04f9eb913f8e2989c14a6fdd2fbddb742bab7fd0; enc_acc=RJfg6sQli8EEexpsPxgoijf3wa9vmllVIBxwsoPA76XUVqIGQlJ+KiddBO8Y1AlbjW6CvFQ2ZIXuUf9Eb1mHLLSjotS4DRDWQ21Ad2Yo5wm6+c7J2/nrCFzmshNT5YAk6T3hJ2auOq1HKgZc8P7Qzkp+ITFg2iBU1YW5ODwusAM=; ecs_acc=RJfg6sQli8EEexpsPxgoijf3wa9vmllVIBxwsoPA76XUVqIGQlJ+KiddBO8Y1AlbjW6CvFQ2ZIXuUf9Eb1mHLLSjotS4DRDWQ21Ad2Yo5wm6+c7J2/nrCFzmshNT5YAk6T3hJ2auOq1HKgZc8P7Qzkp+ITFg2iBU1YW5ODwusAM=; t3_token=5e399e715ccd5da3fda21a021215e7ba; invalid_at=fd958f87db9723b87333b34556099a99e13f004576d8a063f385fb44787e4a3d; third_token=eyJkYXRhIjoiMTMyYzJlNGFmOTFiOWU0ZTRmMmMyMDQwOWVkNWU5NDI2Y2Q0MmM3NDYxZjI1NzgzNTJmYTYwMmM1ZTA3NTBlODMwMzI5YzgyOTJiY2Q0ZmQ2N2I4OTllNTI5NzI3ZDlhYTM5OGViMWVhZGE1MWVmNzkzODViMDAzNWM2MDBlYzc0M2U0ZDIyMmQ1MjM0YzMxMDliMjBjZTAwZmZlNTc2NSIsInZlcnNpb24iOiIwMCJ9; ecs_token=eyJkYXRhIjoiMjA0ZWM1NDcwMThkMjFlOWMyYzRmMzBhNjc5YzZhMTA5ODc5ODJmOGNiZWU1NTJjYjZlMDYzOWZhNTBmZGM1MjE3ZDFkZDBjMTdlOGRmM2UwMzg4YTg3NDA5MDYzMzRmMTQ3NjhlYTJhM2NlODQ5YWJhN2IxODA2MzYxZjdiNzE3M2M3NWZlYTQ1ZTg2NGQ2ZWI0MjFjYjk0YzExYmZkMDdhNmJkNDgwMWVlN2NiNWIyYjE3NTc1ODcwMmUzMTdhOGI4YTkxY2VkNzIxNjRlZmJmYTk2ZTM3ODk4MmUxYTZlYmJlNTYzODVkOTM2MDRjZTkyYmM5N2Q1ZTAwMTkxM2Q3ZDYyMWM2MWYwNzg1Y2EwYWFkNzY0MGQ3ZDhlZDdhZDBhZGIwYmZkYTUyMzMzYmY2NzQzOTYwZWJlM2I1MWZhODhjNzc5YWM1ZDIyZmM1NDdjMzQ4ODJjMGQ4ZGIwMiIsInZlcnNpb24iOiIwMCJ9; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIxNzYwNjUzNzcyNyIsInBybyI6IjAzNiIsImNpdHkiOiIzNjAiLCJpZCI6ImNhZTE4ZDcyNTI1MjcxNDM4YjQxY2MwOWQwNzBmNDUyIn0.6iX9wQuCqCfh6y2G0ATHIjsLS0zyA-cbFkiiUwVJh0M; SHAREJSESSIONID=119812BBC4825E9FE1B64452BB432987; acw_tc=7ae4439c16863141700762552e6c21c84271e1441023473ff420388af9',
        }

        data = {
            'shareCl': '',
            'shareCode': '',
        }

        response = requests.post('https://act.10010.com/SigninApp/signin/daySign', cookies=cookies, headers=headers,
                                 data=data)
        print(response.text)
        j = json.loads(response.text)
        R = ''
        if j['status']=='0000':
            for n in j['data']['sevenDaysResultMap']['sevenDaysList']:
                if n['signFlag']=='1':
                    R = R + '\n'+n['days']+":签到成功"
                else:
                    R = R + '\n' + n['days'] + ":未签到"
        else:
            R = R+"\n"+j['msg']
        R = R+'\n'
        return R
