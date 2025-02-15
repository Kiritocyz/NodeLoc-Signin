# -- coding: utf-8 --
import os
import sys
from curl_cffi import requests

NS_RANDOM = os.environ.get("NS_RANDOM","true")
NS_COOKIE = os.environ.get("NS_COOKIE","")
COOKIE = os.environ.get("COOKIE", "")
userId = os.environ.get("USERID", "")
x_token = os.environ.get("X_TOKEN", "")
COOKIE_ENV = NS_COOKIE or COOKIE

pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
chat_id = os.environ.get("CHAT_ID","")
thread_id = os.environ.get("THREAD_ID","")
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代
def telegram_Bot(token,chat_id,message):
    url = f'{telegram_api_url}/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'message_thread_id': thread_id,
        'text': message
    }
    r = requests.post(url, json=data)
    response_data = r.json()
    msg = response_data['ok']
    print(f"telegram推送结果：{msg}\n")
def pushplus_ts(token, rw, msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data)
    msg = r.json().get('msg', None)
    print(f'pushplus推送结果：{msg}\n')

def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            hadsend=True
        except:
            print("加载notify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        print("加载通知服务失败,缺少notify.py文件")
        hadsend=False
load_send()

if COOKIE_ENV:
    url = f"https://www.nodeloc.com/api/users/{userId}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        'sec-ch-ua': "\"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"122\", \"Chromium\";v=\"122\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
	'origin': "https://www.nodeloc.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.nodeloc.com/",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
	'Connection': "keep-alive",
	'X-Csrf-Token': x_token,
	'X-Http-Method-Override': "PATCH",
        'Cookie': COOKIE_ENV
    }

    try:
        response = requests.post(url, headers=headers,impersonate="chrome110")
        response_data = response.json()
        print(response_data)
        print(COOKIE_ENV)
        message = response_data.get('message')
        success = response_data.get('success')
        # send("bincloud登录", message)
        if success == "true":
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
        else:
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
            if pushplus_token:
                pushplus_ts(pushplus_token, "bincloud登录", message)
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text)
        # if telegram_bot_token and chat_id:
            # if "Mike Hand" in response.text:
                # telegram_Bot(telegram_bot_token, chat_id, "✅BinCloud登录成功!")
            # else:
                # telegram_Bot(telegram_bot_token, chat_id, "❌登录BinCloud失败了!")
else:
    print("请先设置Cookie")
    # if telegram_bot_token and chat_id:
        # telegram_Bot(telegram_bot_token, chat_id, "❌BinCloud的cookie已失效，请重新抓取!")
