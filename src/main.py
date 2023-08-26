from flask import Flask, send_file, jsonify
import requests, json, time

token = input("Acc token: ")

app = Flask(__name__)

session = requests.Session()

response = session.get('https://discord.com/api/v9/users/@me/burst-credits')

def sendFr(userID):
    res = session.put('https://discord.com/api/v9/users/@me/relationships/'+userID, headers={
        'authority': 'discord.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Linux',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'Europe/Zagreb',
        'x-super-properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAuMC4wIiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiJodHRwczovL2Rpc2NvcmQuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6ImRpc2NvcmQuY29tIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjIyOTYzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    }, json={})

    status = res.status_code

    if(status == 401): 
        exit()

    if(status == 429): # if rate limit try again in 10sec
        time.sleep(10)
        sendFr(userID)

    return status

@app.route('/')
def indexpage():
    return send_file("index.html")

@app.route('/add/<string:userID>', methods=['GET']) # get is faster then post?
def get_item_by_name(userID):
    return str(sendFr(userID))


# this whole project should have been made in electron.js
@app.route('/pfp.webp', methods=['GET'])
def defPfp():
    return send_file("../assets/defaultPfp.webp")

@app.route('/style/style.css', methods=['GET'])
def getStyle():
    return send_file("style/style.css")

@app.route('/js/main.js', methods=['GET'])
def getJs():
    return send_file("js/main.js")

# make back up file
def makeBackUp():
    response=requests.get("https://discord.com/api/v9/users/@me/relationships", headers={'authorization': token})
    
    file = open("data.json", "a+")
    file.write(json.dumps(json.loads(response.text), indent=4))
    file.close()

def main():
    if(int(input("1. Make BackUp\n2. Start GUI\ninp: ")) == 1):
        makeBackUp()
    else:
        app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()