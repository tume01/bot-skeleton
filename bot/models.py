# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.conf import settings
from django_mysql.models import Model, JSONField
from django.db import models
from typing import Dict
from enum import Enum
from model_utils import Choices


class Message(TimeStampedModel, Model):

    text = models.CharField(
        max_length=5000,
        help_text='user message',
        blank=True,
        null=True,
    )

    recipient_id = models.CharField(
        max_length=200,
        help_text='user id',
    )

    sender_id = models.CharField(
        max_length=200,
        help_text='user id',
    )

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS


class Conversation(TimeStampedModel):

    START_STATUS = 1

    CONVERSATION_STATUS = Choices(
        (START_STATUS, 'inicio'),
    )

    status = models.IntegerField(
        choices=CONVERSATION_STATUS,
        default=START_STATUS,
    )

    recipient_id = models.CharField(
        max_length=200,
        help_text='user id',
    )

    sender_id = models.CharField(
        max_length=200,
        help_text='user id',
    )

    class Meta:
        ordering = ['-created']
        default_permissions = settings.API_PERMISSIONS

class EventMessage(object):

    def __init__(self, sender_id: str, recipient_id: str, timestamp: str):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.timestamp = timestamp

class FacebookTextMessageType(Enum):
    PLAIN_TEXT = 1
    QUICK_REPLY = 2

class FacebookTextMessage(EventMessage):

    def __init__(self, sender_id: str, recipient_id: str, timestamp: str, message:str, text_type: FacebookTextMessageType):
        super(FacebookTextMessage, self).__init__(sender_id, recipient_id, timestamp)
        self.text = message
        self.type = text_type

class FacebookMediaType(Enum):
    FILE = 1
    AUDIO = 2
    IMAGE = 3
    VIDEO = 4

class FacebookMediaMessage(EventMessage):

    def __init__(self, sender_id: str, recipient_id: str, timestamp: str, media_type: FacebookMediaType, payload_url: str):
        super(Handler, self).__init__(sender_id, recipient_id, timestamp)
        self.media_type = media_type
        self.payload_url = payload_url



