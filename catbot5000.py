from datetime import datetime
from dateutil import parser
import requests
import json
from flask import Flask, request, abort
from mysecrets.mysecrets import chatbotsecrets as CBS

api_url = 'http://192.168.2.4:8080'

app = Flask(__name__)

FILE_TO_WRITE_TO = CBS['FILE']
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        message = request.json.get('eventData').get('body')
        user = request.json.get('eventData').get('user').get('displayName')
        timestamp = request.json.get('eventData').get('timestamp')
        formatted = datetime.strftime(parser.isoparse(timestamp), '%H:%M:%S')

        if user and message and timestamp:
            write_out_chatlog(formatted, user, message)
            handle_message(user, message)

        return 'success', 200
    else:
        abort(400)

def handle_message(_user, _message):
    cmdflag = _message[0]
    words = _message.split(" ")
    cmd = words[0][1:]
    if cmdflag == "!":
        handle_bang_commands(_user, cmd, words)

def handle_bang_commands(_user, _cmd, words):
    if _cmd == "funk":
        reply(_user + " is going to funk you up.")
        
    elif _cmd == "walrus":
        reply(_user + " is the walrus.")

    elif _cmd == "tron":
        reply("Catbot5000 fights for the users.")

    else:
        reply("What you talkin about " + _user + "?")

def reply(_str):
    msg = {
        'headers': {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + CBS["CHATBOT_TOKEN"],
        },
        'message' : {'body': _str},
    }

    r = requests.post(api_url+"/api/integrations/chat/send", 
                        data=json.dumps(msg['message']), 
                        headers=msg['headers']
                    )
    print(r)
    pass

def write_out_chatlog(timestamp, user, message):
    with open(FILE_TO_WRITE_TO, mode='a') as chatlog:
        chatlog.write(f"{timestamp} {user}: {message}\n")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

