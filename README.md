# APM-r128gain
b站视频音量增益收集

这是[APM](https://github.com/lovegaoshi/azusa-player-mobile)上传的b站r128gain音量增益数值集合。

内容见https://github.com/lovegaoshi/APM-r128gain/blob/main/rules.json

格式为[{itemid: b站CID, r128gain: 音量增益数值, abrepeat: 掐头去尾}]

itemid: string

r128gain: Number | string (用Number()转)

abrepeat: json.stringify([number, number])
