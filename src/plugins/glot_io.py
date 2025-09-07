### 调用Glot.io跑代码
import requests
import json

def run_python(code: str):
    payload = {
        "command": "",
        "files": [{
            "name": "main.py",
            "content": code
        }],
        "stdin": ""
    }

    payload_json = json.dumps(payload)

    req = requests.post(
        "https://glot.io/run/python?version=latest",
        payload_json
    )

    resp = req.json()
    stdout = resp["stdout"]
    stderr = resp["stderr"]
    return stdout, stderr
