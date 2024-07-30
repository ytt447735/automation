import base64
import urllib
import requests
import ujson

# 百度手写识别key
API_KEY = ""
SECRET_KEY = ""


def get_manage(base64):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\segment_1.png",True) 方法获取
    payload = {
        "image": base64,
        "detect_direction": "false",
        "probability": "false",
        "detect_alteration": "false"
    }
    # payload = 'image=iVBORw0KGgoAAAANSUhEUgAAAEgAAABYCAIAAADZWSaLAAAIt0lEQVR4nO1bf0iTzx%2B%2FfcdYIiIjZISYyLAVIhEjRCxkmVhIiZnIEBkyRCRKJMWGxBgyRCKGyIgYYiEmERLDxggRMREbMkS0Yo0xZMiQKRJD1hC5zx%2F3%2Fd7n7T3PfjzPZrkve%2F2159537%2Ff7dfc8d%2Fd%2B302CMUb%2Fj%2FjP33bgtJAjlm3IEcs25IhlG3LEsg05YtmGHLFsQ47YH8fW1lZ%2Ff%2F%2Fly5dv3bolpj0%2BY3A6ncXFxYyTDQ0NQvVkgJjH40lfCcGjR48yNQDpEqOuHB0dpaNneno68Zul0%2BkEKUyLWDQapYYHBwfFKXG73RqNJukn4%2Ff7BalNi1goFKKGFQrF%2Fv6%2BUA1v377lcpBKpU6nE59MxgjVnBaxQCAAba%2BtrXErtLe3I4Tq6%2BsPDg6gyO%2F35%2BXlcVnV19d7vV6MscfjoYWFhYXRaPSvEdvc3ITS8fFxKDWbzVTkcrm4lFQqVSgUonWqq6up6N69e0J9S%2Fcbg73u8%2FlI%2Bfz8PNfvvr4%2BIp2bm%2BNKLRbL8fEx1by0tASli4uLf5QYxlipVFLzLpdrc3MT9jTEysoKxvj169dMuVwu%2F%2FbtG6O2tLQU1hHhWLrESkpKqPmamhqpVMqlpNfryRcSjUaLioqgaHBwMBaLMTqZGWVqauovEGtoaEAIyWQy3rVVq9W6XC5YH46w1WpVq9UIoa6urhM%2BAVy9elWcY2kROz4%2B7uzsbG1t9fv9Xq%2BXYbW0tMRt4na7idRsNsPZxWQyMRUIRHxdBOKJDQ8PI4Sampr%2B1fU%2F9Pb2pqJhdHQUctjY2MAYP3%2F%2BHBaKdk9My%2B3t7Zs3bxLDAwMDpJDMhBqNZnZ2NkU9a2trkMPTp0%2Fxyfewo6NDhHsEgolNTU1B27W1tRsbGz09PXl5eaOjo0K1wfHJz8%2FHnKMfnU4XDAaFqsWCiAWDwWvXrqH4WFhYEGr%2B8PAQanA6nZnSnCoxn8%2FHrC0Iod7eXolEQh%2B5rY6Pj%2Bfm5paXlxNolslkVENTUxOzX6H49etX5oltb28zZiQSicPhwCffnPX1daahTqcjosLCQrfbzavcarVCJRjjcDjc2NjIWKysrMwwMa1Wy9hobW39tz0AoUoQiUTOnz%2FPNAwEAlz9kUiEIUYQDAabmpqgaH5%2BPjPEgsHg9evXGefogoMx9vl8UEQ3wSsrK4gPWq2W3wmE6A7mxYsXjIhCIpGkHpUlIlZeXs54ZjQaYYX19XVuZ%2Fv9fl5WBHD%2FTnB0dGQwGBYWFoi2srIyGIy%2FfPkSNq%2BqqkqX2MePHxmfZmZmuD5xiV24cCEBsbGxMa6toaGhlpYWjLHD4WhubmaGpa2tDWrY2dlJixgM%2B%2BN9uGazmdbRaDTBYFChUEAnJBKJ1%2BttaWlJ3OXLy8u0X0Kh0MjICOslgFqtjkQi4olhjA8PD9vb200mUzxFVVVVkFh9fT30oLq6mlRjwjNeVdXV1T9%2B%2FKA0VldXodRut0MNVqs1LWJJwf0IISsYzEMRDCgpZmdntVotmffKysqKi4uZ7S9M%2BCiVylMkBt9VLsLh8AkzALzx1cbGBpGura1ZLBbyG37V5HVNPOyZIQbdvXLlCrT6%2BfNnWofsGOrq6qiUN60bjUYrKytJBchhenqaaw4hlHQDKZ7Y5uYmNZOfn09%2Fz83N4ZOTqsPhmJiYSNrfcCqCMBqNZAEgUSnB0NDQaREzmUwIodLS0p2dndraWmJveHgYY8zQqKioYN5bXoXv37%2FnJYYQUqvVHo%2Fn8ePHtEShUJwWMYPBgBBaXV2lO3Sr1RoIBPR6PeMWiTthCe9unQnPYDaFt%2BS0iEHtCCGtVkvGkEFVVRWZHsvKymhhZ2cnV%2BH%2B%2Fj5M9djtdmZ%2FzOBUiO3u7hLtMzMzRqMxnu3JyUmMcSQSmZiYgGu3TCbjVUveAoJXr17hOKlVhFB3d%2FepEGtubiYGysvL4%2B2hPnz4QCqTTFYq%2FW2z2WiFuro6Uri4uMhtzmSdM0MsFosVFhYylmDutq%2Bvj25W4uVPadoYghmf7e1tUj47OwvLmQggY8TgRA9HoKCgAIGVx%2B1206WJCzJ%2FMmDiIJjAC4fDNpstXrSaGWK9vb1cR0k6pKenh9RhZnyEkEqlgut4vEwoHGFxOWDxxKC7TExht9sxX8iDEPJ6vcxKxat8cHCQVtDr9X%2BOGJ0PCcbHx2mOESGk0%2Bm6u7u5rOhuPSkxuJEvKCgQcZgokhjzjkWj0cnJSS4TBjTPAwt5c%2BDMARJJD4uA4Hse7969o7%2B7urrOnTuXyj2MGzdufP%2F%2BnSn88uULt%2BalS5fg4%2B%2Ffv4V6%2BF8I7QnYllyEgCfREDabDe5FlEplOBwmJ7cEjY2NvCZUKhWt84cOJeBUIZfLScgYDochn7t378IQE06hFRUVDoeDPpaUlPBagUlFOs2eIjFmkaFnykw6ta2tjWkol8upFG5TiouLeY%2FMyTkOgVQqPXViTCbshBYAlUrFNGSSWRA0zwHB7KFEsMKCiEFjFoslngghxD1THhkZ4SUWL7mbPrFUZ8WvX7%2FCxzt37sBHGPkjhLa2tpjmz5496%2Bzs5Krd29vjNQcPQN68eZOikyeQYgfAnQ43SQSnBIQQNzHIHYfENWEvaDSa1AeKIqUR%2B%2FTp0%2BrqKn188uQJU%2BH%2B%2FftDQ0P08eLFi7x6uDn9nz9%2F8ta8ffs2%2FQ2v6AhAYt6xWIx7LhGvMgndZTJZgiz0wMAAVFVTU8NbjVkbUxwliCRtxsbGGFZkmxsPXq93d3c3sU44kdBglMczgKRhJU%2FzxOKOjg6GGA3%2B0gHpL%2BZ6BwOa%2BUIIGQwGoSaSEGMOTpNmGjIIuEyLeBuTNDg4OKAH6lKpNJVjjkyBycYJbZ68Abl%2Bk5eXl3pYnilAYkKv5p65W9wQ8M4gycaljrN77x4h9ODBA%2FobxoGp4EwT6%2B%2Fvp%2FdIHj58KKitBJ%2FtP3jv7e0VFRWJcPKsExONM%2F0qpoMcsWxDjli2IUcs25Ajlm3IEcs25IhlG%2F4BarRllGnmfvIAAAAASUVORK5CYII%3D&detect_direction=false&probability=false&detect_alteration=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    j = ujson.loads(response.text)
    return j['words_result_num']


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
