from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Student, LineMessage
from linebot import LineBotApi

from utils import manaba_scrape
from line_bot_ai.line_message import LineBotApi

with open("secret.json", "r") as f:
    ACCESSTOKEN = json.load(f)['ACCESSTOKEN']

line_bot_api = LineBotApi

@csrf_exempt
def callback(request):
    if request.method == "POST":
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_user_id = events[0]['source']['userId']

        # チャネル設定のWeb hook接続確認時にはここ。このIDで見に来る。
        if line_user_id == 'torikeme4':
            pass

        # 友達追加時・ブロック解除時
        elif events[0]['type'] == 'follow':
            Student.objects.create(user_id=line_user_id, display_name=profile.display_name)

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            Student.objects.filter(user_id=line_user_id).delete()
        
        # メッセージ受信時
        elif events[0]['type'] == 'message':
            text = request_json['events'][0]['message']['text']
            line_push = get_object_or_404(Student, user_id=line_user_id)
            LineMessage.objects.create(push=line_push, text=text, is_admin=False)

    return HttpResponse()
