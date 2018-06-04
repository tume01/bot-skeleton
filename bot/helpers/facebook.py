from typing import Dict, List
from django.conf import settings
import requests


class FacebookHelper(object):

    @staticmethod
    def send_message(recipient_id: str, message: str) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {'text': message},
        }

        r = requests.post(settings.FACEBOOK_GRAPH_URL, params=params, json=data)
        return r.status_code == 200

    @staticmethod
    def post_back_button(title, payload) -> Dict[str,str]:
        return {
            'type': 'postback',
            'title': title,
            'payload': payload
        }

    @staticmethod
    def send_buttons(recipient_id: str, message: str, buttons: List[Dict[str,str]]) -> bool:
        params = {
            'access_token': settings.BOT_APP_TOKEN
        }

        data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': message,
                        'buttons': buttons,
                    }
                }
            }
        }
        r = requests.post(settings.FACEBOOK_GRAPH_URL, params=params, json=data)
        return r.status_code == 200