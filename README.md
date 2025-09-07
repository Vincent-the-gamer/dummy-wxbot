# dummy-wxbot

用笨办法实现的微信小bot，采用Webhook消息推送 + ADB自动化实现。

_PS: 原则上这种方法可应用于任何聊天软件_

## 需要安装的安卓软件

必须安装：
- [SmSForwarder](https://github.com/pppscn/SmsForwarder): 用于转发通知到Webhook
- [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard): 需要借助它实现自动化中文输入，因为`adb shell input text`不能输入中文，此外，需要在微信中关闭回车换行，即让回车变为发送消息

可选安装:
- [EasyTier](https://github.com/EasyTier/EasyTier)：用于内网穿透

## 使用该项目

1. 大模型接入的是[GPTGod](https://gptgod.site/)的服务，在项目根目录创建`.env`文件，填入大语言模型的token即可：
```dotenv
token=xxxx
```

2. 启动`src/webhook.py`
3. 到**SmSForwarder**配置Webhook，指向你自己的webhook，注意**消息模板的配置**

![消息模板1.png](.github/%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF1.png)

4. **SmSForwarder**配置消息转发规则： 当App包名是：`com.tencent.mm`时转发到webhook，注意**自定义模板的配置**

![消息模板2.png](.github/%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF2.png)

5. 使用`adb`无线连接到安卓手机
6. 切换输入法至**ADBKeyBoard**，将微信打开到你要进行交互的对话框，然后点击输入框，记得提前设置关闭回车换行，即让回车变为发送消息

![wx2.png](.github/wx2.png)
![wx1.png](.github/wx1.png)

5. 回到**SmSForwarder**，一切准备就绪，这时可以开始交互了

## 交互

使用`/help`查看指令列表。

## 演示

https://github.com/user-attachments/assets/e75611f7-8ce1-497c-ae88-25c961777393


## 开源证书

[MIT 证书](./LICENSE.md)

Copyright (C) 2025-present Vincent-the-gamer
