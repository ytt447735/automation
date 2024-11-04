#### 功能
| 名称     | 功能                                                                      | 变量获取                          | 变量名 | 变量模版 |
|:-------|:------------------------------------------------------------------------|:------------------------------|:------------------------------|:------------------------------|
| wps pc | pc端签到领取兑换vip时间<br/> 云空间签到领取容量<br/>| [获取](https://vip.wps.cn/home) | wps_pc | wpsua=***;wps_sid=***;day=1 |
| OPPO积分 | OPPO商城签到、每日任务 | Reqable抓包获取CK | OnePlus_COOKIE | TOKENSID=***;apkPkg=*** |
| 贝锐 | 阳光小店每日签到、每日任务 | [获取](https://www.oray.com/) | BR_COOKIE | _s_id_=*** | 

---
#### 使用
<details> <summary>青龙面板</summary>

##### 拉库
```
ql repo https://github.com/ytt447735/automation.git  fun|notify.py fun main py
```
##### 环境变量
PC(day等于每日签到时自动兑换天数，可不设)：
```
wps_pc
wpsua=***;wps_sid=***;day=1
```
##### 依赖
```
ujson
requests
```
#### 验证码识别配置
之前版本采用的是百度的手写文字识别功能，[获取](https://console.bce.baidu.com/ai/?_=1722298138766#/ai/ocr/overview/index)
在"/fun/baidu.py"文件内修改"API_KEY"、"SECRET_KEY"的值<br/>
百度识别准确率低，已替换，原代码保留着，可自行替换<br/>
新代码已采用YOLOv8模型识别，准确率98%左右，识别模型代码暂不开放，识别接口暂免费提供<br/>

#### CK失效
目前测试发现CK好像不会过期，一直有效
</details>

---
#### 预览
<details> <summary>WPS</summary>

![WPS](image/3.png)
</details>
