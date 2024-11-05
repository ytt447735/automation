import time
import re

# 获取时间戳
def get_time():
    return int(round(time.time() * 1000))

# 取中间文本
def GetIntermediateText(text, start, end):
    print(text)
    pattern = re.escape(start) + '(.*?)' + re.escape(end)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''
