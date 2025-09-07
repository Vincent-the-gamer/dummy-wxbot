### 用于接收来自安卓手机SmSForwarder推送的微信消息
from time import sleep
from flask import Flask, request, jsonify
from sender import send_wechat_msg, open_wechat, open_forwarder
from plugins.deepseek import mesugaki_txt, deepseek_chat, neko_txt

app = Flask(__name__)

roles = {
    "雌小鬼": mesugaki_txt,
    "猫娘": neko_txt
}

payload = {
   "model": "deepseek-r1",
   "messages": [
      {
         "role": "system",
         "content": roles["雌小鬼"]
      },
   ],
   "stream": False
}

@app.route('/')
def get_wechat_msg():
    msg = request.args.get('msg')
    # 目前群消息格式：[4条]天堂制造: （
    # 私聊则是直接发送消息，所以要做判断
    if ":" in msg:
        msg = msg.split(":", 1)[1].strip()

    # 帮助
    if '/help' in msg:
        msg = msg.replace('/help', '').strip()
        resp = """可用指令：
    查看帮助：/help
    测试连通性: /hello
    调用AI对话: /ai <对话内容>
    查看角色列表: /list_role
    切换角色: /role <角色名称>"""
        open_wechat()
        sleep(1)
        send_wechat_msg(resp)
        sleep(1)
        open_forwarder()


    # 问候
    if '/hello' in msg:
        msg = msg.replace('/hello', '').strip()
        open_wechat()
        sleep(1)
        send_wechat_msg(f"{msg}你好啊！Ciallo～(∠・ω< )⌒★!")
        sleep(1)
        open_forwarder()

    # AI调用
    elif '/ai' in msg:
        msg = msg.replace('/ai', '')
        open_wechat()
        sleep(1)
        resp = deepseek_chat(payload, msg).strip()
        send_wechat_msg(resp)
        sleep(1)
        open_forwarder()

    # 显示角色
    elif '/list_role' in msg:
        resp = "使用 /role <角色名> 来切换角色\n 当前可用角色有：\n"
        for key in roles:
            resp += key + "\n"
        open_wechat()
        sleep(1)
        send_wechat_msg(resp)
        sleep(1)
        open_forwarder()

    # 切换角色
    elif '/role' in msg:
        msg = msg.replace('/role', '').strip()
        if msg in roles:
            payload["messages"][0]["content"] = roles[msg]
            open_wechat()
            sleep(1)
            send_wechat_msg(f"切换角色成功！当前角色：{msg}")
            sleep(1)
            open_forwarder()
        else:
            open_wechat()
            sleep(1)
            send_wechat_msg("可用角色中没有该角色！")
            sleep(1)
            open_forwarder()


    return jsonify({
        'received_msg': msg,
        'code': 200
    })


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
    )
