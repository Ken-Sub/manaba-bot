from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .line_bot_manage import LineMessage

from utils.manaba_scrape import arrange_manaba_scrape_result

import json
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ButtonsTemplate,
    PostbackAction, MessageAction, URIAction
)


def get_info():
    with open('core/secret.json', 'r') as f:
        info = json.load(f)
    return info

def send_register_form(num):
    buttons_template_message = TemplateSendMessage(
        alt_text='ボット登録',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='ボット登録',
            text='manabaのログインIDとPASSWORDを登録してください。',
            actions=[
                URIAction(
                    label='uri',
                    uri='http://example.com/' # numでstudentのidを取得しeditのurlに反映
                )
            ]
        )
    )
    return buttons_template_message

@csrf_exempt
def callback(request):
    if request.method == "POST":
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        reply_token = events[0]['replyToken']
        line_user_id = events[0]['source']['userId']
        line_display_name = events[0]['source']['display_name']

        # チャネル設定のWeb hook接続確認時にはここ。このIDで見に来る。
        # if line_user_id == 'torikeme4':
        #     pass

        # 友達追加時・ブロック解除時
        if events[0]['type'] == 'follow':
            Student.objects.create(user_id=line_user_id, name=line_display_name)
            buttons_template_message = send_register_form()
            line_message = LineMessage(buttons_template_message)
            line_message.reply(reply_token)

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            Student.objects.filter(user_id=line_user_id).delete()
        
        # メッセージ受信時
        elif events[0]['type'] == 'message':
            student = Student.object.filter(user_id=line_user_id)
            if not student:
                buttons_template_message = send_register_form()
                line_message = LineMessage(buttons_template_message)
                line_message.reply(reply_token)
            else:
                manaba_id = student.manaba_id
                manaba_password = student.manaba_password
                text = request_json['events'][0]['message']['text']
                if text == "課題確認":
                    result = arrange_manaba_scrape_result(manaba_id, manaba_password)
                    message = TemplateSendMessage(text=result)
                    line_message = LineMessage(message)
                    line_message.reply(data)
                else:
                    message = TemplateSendMessage(text="「課題確認」と入力してください。")
                    line_message = LineMessage(message)
                    line_message.reply(data)

    return HttpResponse()

def edit(request, num):
    obj = Student.objects.get(id=num)
    if request.method == "POST":
        student = StudentEditForm(request.POST, instance=obj)
        student.save()
        return redirect(to="/success")
    params = {
        'title': 'manabaログイン情報フォーム',
        'student': obj,
        'id': num,
        'form': StudentEditForm()
    }
    return render(request, 'linebot_api/edit.html', params)

def success(request):
    params = {
        'title': '登録完了',
        'text': '次回からは「課題確認」のメッセージを送信するだけで未提出課題の取得を行います。'
    }
    return render(request, 'linebot_api/success.html', params)