### 用于接收来自安卓手机SmSForwarder推送的微信消息
import re
from time import sleep
from flask import Flask, request, jsonify
from sender import send_wechat_msg, open_wechat, open_forwarder
from plugins.deepseek import mesugaki_txt, deepseek_chat, neko_txt
from plugins.glot_io import run_python
from src.plugins.deepseek import default_txt

app = Flask(__name__)

roles = {
    "DeepSeek": default_txt,
    "雌小鬼": mesugaki_txt,
    "猫娘": neko_txt
}

current_role = "DeepSeek"

payload = {
   "model": "deepseek-r1",
   "messages": [
      {
         "role": "system",
         "content": roles["DeepSeek"]
      },
   ],
   "stream": False
}

@app.route('/')
def get_wechat_msg():
    global current_role
    msg = request.args.get('msg')
    # 目前群消息格式：[4条]天堂制造: （
    # 私聊则是直接发送消息，所以要做正则过滤
    group_pattern = r'^\[\d+条\][^:]+:\s*(.*)$'
    match = re.match(group_pattern, msg)

    if match:
        # 群消息，提取消息内容
        msg = match.group(1)

    # 帮助
    if '/help' in msg:
        msg = msg.replace('/help', '').strip()
        resp = """可用指令：
    查看帮助：/help
    测试连通性: /hello
    调用AI对话: /ai <对话内容>
    查看角色列表: /list_role
    切换角色: /role <角色名称>
    查看当前角色: /current_role
    跑Python代码: /python <代码>"""
        open_wechat()
        sleep(1)
        send_wechat_msg(resp.strip())
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
        resp = "使用 /role <角色名> 来切换角色\n当前可用角色有：\n"
        for key in roles:
            resp += key + "\n"
        open_wechat()
        sleep(1)
        send_wechat_msg(resp.strip())
        sleep(1)
        open_forwarder()

    # 切换角色
    elif '/role' in msg:
        msg = msg.replace('/role', '').strip()
        current_role = msg
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

    # 跑代码
    elif '/python' in msg:
        msg = msg.replace('/python', '').strip()
        stdout, stderr = run_python(msg)
        open_wechat()
        sleep(1)
        message = f"stdout: \n{stdout} \nstderr: \n{stderr}"
        send_wechat_msg(message)
        sleep(1)
        open_forwarder()

    elif '/current_role' in msg:
        msg = msg.replace('/current_role', '').strip()
        open_wechat()
        sleep(1)
        send_wechat_msg(f"当前角色：{current_role}")
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
