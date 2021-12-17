import requests, time, cloudscraper, random, json, threading


# messages you want to send, separated by a comma
messages = [""]
# page url of the user on tellonym
pageurl = ''
# apikey from capmonster.cloud
apikey = ''
# how many threads you want to run the bot
threads = 5


userAgent = {"user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

def get_user_id(scr):
    name = pageurl.split("/")[3]
    usrId1 = scr.get("https://api.tellonym.me/profiles/name/"+str(name)).json()
    return usrId1["id"]

userid = get_user_id(cloudscraper.create_scraper())
userid = userid

def get_random_message():
    return random.choice(messages)

def random_proxy():
    with open("proxies.txt", "r") as f:
        x = f.readlines()
        proxies = [i.strip() for i in x]
        return random.choice(proxies)

def fetchproxy():
    x = random_proxy()
    return str(x)

def get_captcha():

    sitekey = "494aec4c-f02d-462c-9a37-606425aa6769"

    payload = {

        "clientKey":apikey,
        "task" : {
            "type" : "HCaptchaTaskProxyless",
            "websiteUrl": pageurl,
            "websiteKey":sitekey,
        }
    }

    session = requests.session()

    one = session.post("https://api.capmonster.cloud/createTask", json=payload).text
    id = json.loads(one)["taskId"]
    print(f"STATUS | Token {id}")


    while True:

        time.sleep(6)

        payload2 = {
        "clientKey":apikey,
        "taskId": id
        }

        two = session.get("https://api.capmonster.cloud/getTaskResult", json=payload2).text
        
        if 'CAPTCHA_NOT_READY' in json.loads(two)["status"]:
            print("STATUS | still waiting for captcha..")

        elif 'ERROR_CAPTCHA_UNSOLVABLE' in json.loads(two):
            print("ERROR | captcha error.")
            break

        elif json.loads(two)["status"] == "ready":
            return json.loads(two)["solution"]["gRecaptchaResponse"]

def thread():

    message = get_random_message()

    proxy = fetchproxy()

    proxies = {"http://" : f'http://{proxy}', "https://" : f'https://{proxy}'}

    cld = cloudscraper.create_scraper()

    url = "https://api.tellonym.me/tells/new"

    captchakey = get_captcha()

    data = {
        "hCaptcha": captchakey,
        "pressContentCount": 0,
        "previousRouteName": "Profile",
        "limit": 25,
        "contentType": "CUSTOM",
        "":""
        "isInstagramInAppBrowser: false",
        "isSenderRevealed": "false",
        "tell": message,
        "userId": userid,
    }

    one = cld.post(url, data=data, headers=userAgent, proxies=proxies)
    if one.status_code == 200:
        print(f'SUCCESS | sent a message - {message}')
    else:
        print(one.text)
    return ''

for i in range(threads):
    t = threading.Thread(target=thread, args=())
    t.start()