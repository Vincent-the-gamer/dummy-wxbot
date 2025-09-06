### 用于接收来自安卓手机SmSForwarder推送的微信消息
from time import sleep
from flask import Flask, request, jsonify
from sender import send_wechat_msg, open_wechat, open_forwarder
from plugins.deepseek import mesugaki_txt, deepseek_chat
import json
app = Flask(__name__)

payload = json.dumps({
   "model": "deepseek-r1",
   "messages": [
      {
         "role": "system",
         "content": mesugaki_txt
      },
   ],
   "stream": False
})

@app.route('/')
def get_wechat_msg():
    msg = request.args.get('msg')
    # 目前群消息格式：[4条]天堂制造: （
    # 私聊则是直接发送消息，所以要做判断
    if ":" in msg:
        msg = msg.split(":", 1)[1].strip()


    # 问候
    if '/hello' in msg:
        print(f"调用了/hello, 消息: {msg}")
        msg = msg.replace('/hello', '')
        open_wechat()
        sleep(1)
        send_wechat_msg(f"{msg}，你好啊！Ciallo～(∠・ω< )⌒★!")
        sleep(1)
        open_forwarder()

    elif '/ai' in msg:
        print(f"调用了/ai, 消息: {msg}")
        msg = msg.replace('/ai', '')
        open_wechat()
        sleep(1)
        resp = deepseek_chat(payload, msg).strip()
        send_wechat_msg(resp)
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
