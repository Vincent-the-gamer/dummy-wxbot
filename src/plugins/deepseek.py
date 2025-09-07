import http.client
import json
import os
from dotenv import dotenv_values

env_vars = dotenv_values()

current_path = os.path.abspath(os.path.dirname(__file__))

# 雌小鬼守则
mesugaki = open(os.path.join(current_path, "../prompts/雌小鬼守则.txt"), "r")
mesugaki_txt = mesugaki.read()

# 猫娘
neko = open(os.path.join(current_path, "../prompts/猫娘.txt"), "r")
neko_txt = neko.read()

headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer { env_vars["token"] }'
}

def deepseek_chat(payload: dict, msg: str):
    messages = payload["messages"]
    messages.append({
        "role": "user",
        "content": msg
    })
    payload_new = json.dumps(payload)
    conn = http.client.HTTPSConnection("api.gptgod.online")
    conn.request("POST", "/v1/chat/completions", payload_new, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    return_msg = result["choices"][0]["message"]["content"]
    return return_msg

