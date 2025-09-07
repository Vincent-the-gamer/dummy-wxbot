# 使用电脑有线连接安卓手机, 或者无线连接adb，然后通过adb实现微信消息发送
import subprocess
from time import sleep

# 要借助ADB输入法才能完成中文输入！
# https://github.com/senzhk/ADBKeyBoard
# 如果您的安卓手机是无线调试，请先在命令行连接：adb connect ip:port

def open_forwarder():
    subprocess.call('adb shell am start -n com.idormy.sms.forwarder/com.idormy.sms.forwarder.core.BaseActivity', shell=True)

def open_wechat():
    subprocess.call("adb shell am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI", shell=True)

def to_home():
    subprocess.call("adb shell input keyevent KEYCODE_HOME", shell=True)

def send_wechat_msg(msg: str):
    cmd = [
        'adb', 'shell', 'am', 'broadcast',
        '-a', 'ADB_INPUT_TEXT',
        '--es', 'msg', f'"{msg}"'
    ]
    subprocess.run(cmd, check=True)
    sleep(1)
    subprocess.call("adb shell input keyevent KEYCODE_ENTER", shell=True)