import requests
import json
import re
import base64

# 识别验证码
def identify(mo,code,model):
    url = f"http://cn-hk-bgp-4.ofalias.net:50818/inference_wps_{mo}"
    payload = code
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'text/plain',
        'source': '1',
        'model': model
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    j = response.text.replace(' ', '').replace('\n', '').replace('\t', '')
    pattern = re.compile(r'\[\[(.*?)\]\]')
    matches = pattern.findall(j)
    print(matches)
    # 38%2C43%7C105%2C50%7C174%2C30%7C245%2C50%7C314%2C34
    # 38,43|105,50|174,30|245,50|314,34
    # 174,40|314,41
    matches = matches[0].replace('],[', '%7C').replace(',', '%2C')
    return matches
