from typing import Any, List, Optional
import bot.utils.messages as messages
from bot.utils.patterns import Handler, Singleton
from bot.helpers.facebook import FacebookHelper
from django.template import loader
from bot.models import EventMessage, FacebookTextMessage, FacebookTextMessageType, Message, Conversation
import datetime


class FacebookGetStartedHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) \
            and request.type is FacebookTextMessageType.QUICK_REPLY \
            and request.text == 'START'

    def perform(self, request: Any) -> None:
        conversation, created = Conversation.objects.get_or_create(
            sender_id=request.recipient_id,
            recipient_id=request.sender_id,
        )
        if FacebookHelper.send_message(request.sender_id, messages.GREETINGS_MESSAGE):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookTextHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return isinstance(request, FacebookTextMessage) and request.type is FacebookTextMessageType.PLAIN_TEXT

    def perform(self, request: Any) -> None:
        if FacebookHelper.send_message(request.sender_id, request.text):
            Message.objects.create(
                text=request.text,
                recipient_id=request.sender_id,
                sender_id=request.recipient_id
            )

class FacebookMediaHandler(Handler):

    def is_valid(self, request: Any) -> bool:
        return False

    def perform(self, request: Any) -> None:
        pass

class MessageHandlerManager(metaclass=Singleton):

    def __init__(self):
        default_handler = FacebookTextHandler()
        media_handler = FacebookMediaHandler(default_handler)
        self.base_handler = FacebookGetStartedHandler(media_handler)

