"""Manage Line bot."""
import os
import json

import dotenv
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ButtonsTemplate,
    URIAction
)
from .models import Student

from utils import bot_message_template
from utils import manaba_scrape

# load .env file
dotenv.load_dotenv()

DEFAULT_BOT_NAME = 'マナバ太郎'
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
ACCESS_TOKEN = os.getenv('ACCESSTOKEN')

class NoEnvKeyError(Exception):
    """No Environment Key Error."""
    pass


if not ACCESS_TOKEN:
    raise NoEnvKeyError('Could not find ACCESSTOKEN key in .env')
else:
    LINE_BOT_API = LineBotApi(ACCESS_TOKEN)


class Bot(object):
    """Base class of Line Bot."""

    def __init__(self, name=DEFAULT_BOT_NAME, user_id='', user_name=''):
        self.name = name
        self.user_id = user_id
        self.user_name = user_name
    
    def reply(self, reply_token, messages):
        """Reply message by Line app"""
        LINE_BOT_API.reply_message(reply_token, messages)

    def hello(self, reply_token):
        """Send hello message to user."""
        temp_file = bot_message_template.get_template('greeting.txt')
        messages = temp_file.substitute({
            'user_name': self.user_name})
        messages = TextSendMessage(text=messages.substitute())
        self.reply(reply_token, messages)

    def tell_message_is_invalid(self, reply_token):
        """Tell user that can't use the message"""
        temp_file = bot_message_template.get_template('wrong_message.txt')
        temp_file = TextSendMessage(text=temp_file.substitute())
        self.reply(reply_token, temp_file)

    def check_message_validation(self, message):
        """Check if the message is valid or not"""
        valid_message = bot_message_template.get_template('valid_message.txt')
        if message in valid_message.substitute():
            return True
        return False


class ManabaBot(Bot):
    """Handle Manaba+R infomation Bot."""

    def __init__(self, name=DEFAULT_BOT_NAME, user_id='', user_name=''):
        super().__init__(name=name, user_id=user_id, user_name=user_name)
        self.student = Student.objects.filter(user_id=self.user_id)
        
    def require_register(self, reply_token):
        """Require fill in the register form"""
        temp_file = bot_message_template.get_template('require_register.txt')
        messages = temp_file.substitute({
            'user_name': self.user_name})
        buttons_template_message = TemplateSendMessage(
            alt_text='ボット登録',
            template=ButtonsTemplate(
                title='ボット登録',
                text=messages,
                actions=[
                    URIAction(
                        label='URL',
                        uri=f'{WEB_HOOK_URL}/linebot-ai/edit/{self.user_id}/{self.user_name}/'
                    )
                ]
            )
        )
        self.reply(reply_token, buttons_template_message)

    def search_homeworks(self, reply_token):
        """scrape manaba+r by stored id and password"""
        if not self.student:
            self.require_register(reply_token)
        else:
            student = Student.objects.get(user_id=self.user_id)
            manaba_id = student.manaba_id
            manaba_password = student.manaba_password
            messages = manaba_scrape.scrape(manaba_id, manaba_password)
            messages = TextSendMessage(text=messages.substitute())
            self.reply(reply_token, messages)

    def remove_student(self):
        if self.student:
            self.student.delete()
