import http.client
import json
import os

src_path = os.path.abspath("./src")

# 雌小鬼守则
mesugaki = open(os.path.join(src_path, "prompts/雌小鬼守则.txt"), "r")
mesugaki_txt = mesugaki.read()

headers = {
   'Content-Type': 'application/json',
   'Authorization': 'Bearer <token>'
}

def deepseek_chat(payload, msg: str):
    payload_dict = json.loads(payload)
    messages = payload_dict["messages"]
    messages.append({
        "role": "user",
        "content": msg
    })
    payload_new = json.dumps(payload_dict)
    conn = http.client.HTTPSConnection("api.gptgod.online")
    conn.request("POST", "/v1/chat/completions", payload_new, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    return_msg = result["choices"][0]["message"]["content"]
    return return_msg

