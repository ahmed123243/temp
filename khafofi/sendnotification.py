import requests
import json


def send_notification(title, message, topic, pageid, pagename):
    url = 'https://fcm.googleapis.com/fcm/send'

    headers = {
        'Authorization': 'key=AAAA96TiMCA:APA91bFb_Enu8p2UFCNMOLaJgBRW0egaWcORUMN5MfWrGyvGs_JVan4iXHjFXkYbl-Nj49XpdWETpmT5IsbSSvQMNjYpcYyf2770tARhRIhI83eC_151dZydYq6qBflNLdCyfYbyjAg-',
        'Content-Type': 'application/json'
    }

    payload = {
        'to': '/topics/' + topic,
        'priority': 'high',
        'content_available': True,
        'notification': {
            'body': message,
            'title': title,
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
            'sound': 'default'
        },
        'data': {
            'pageid': pageid,
            'pagename': pagename
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text
