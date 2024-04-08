import socketio
import requests

http_session = requests.Session()
http_session.verify = False
sio = socketio.Client(http_session=http_session)

BOT_TAG = 'cfxtimes'
BOT_PASSWORD = 'kasha'

def send_message(chat_id, content, reply_to=None, type='default'):
    response = requests.post('https://coffeetox.ru/sendmsgapi', json={
        'tag': BOT_TAG,
        'password': BOT_PASSWORD,
        'content': content,
        'chat_id': chat_id,
        'reply_to': reply_to,
        'type': type
    }, verify=False)

    try:
        json = response.json()

        if 'success' not in json:
            print('There was an error!')
        if 'error' in json:
            print(json['error'])
    except:
        print('Unknown error!')

@sio.event
def message(data):
    send_message(data['chat_id'], data['content'], data['id'])

@sio.on('error')
def handle_server_error(err):
    print('There was an error:', err)
    sio.disconnect()
    exit()

sio.connect('https://coffeetox.ru')
sio.emit('activate_bot_api', {'tag': BOT_TAG, 'password': BOT_PASSWORD})

sio.wait()