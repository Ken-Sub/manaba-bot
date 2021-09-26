import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentEditForm

from .line_bot_manage import ManabaBot
from .line_bot_manage import LINE_BOT_API


@csrf_exempt
def callback(request):
    if request.method == "POST":
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        reply_token = events[0]['replyToken']
        profile = LINE_BOT_API.get_profile(events[0]['source']['userId'])
        line_user_id = profile.user_id
        line_display_name = profile.display_name
        manaba_bot = ManabaBot(user_id=line_user_id, user_name=line_display_name)

        # 友達追加時・ブロック解除時
        if events[0]['type'] == 'follow':
            manaba_bot.hello(reply_token)
            manaba_bot.require_register(reply_token)

        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            manaba_bot.remove_student()
        
        # メッセージ受信時
        elif events[0]['type'] == 'message':
            text = events[0]['message']['text']
            result = manaba_bot.check_message_validation(text)
            if result:
                manaba_bot.search_homeworks(reply_token)
            else:
                manaba_bot.tell_message_is_invalid(reply_token)

    return HttpResponse()

def edit(request, num, name):
    if request.method == "POST":
        student_form = StudentEditForm(request.POST)
        if student_form.is_valid():
            new_student = student_form.save(commit=False)
            new_student.user_id = num
            new_student.user_name = name
            new_student.save()
        return redirect(to="/linebot-ai/success")
    params = {
        'title': 'manabaログイン情報フォーム',
        'user_id': num,
        'user_name': name,
        'form': StudentEditForm()
    }
    return render(request, 'linebot_api/edit.html', params)

def success(request):
    params = {
        'title': '登録完了',
        'text': '次回からは「課題確認」のメッセージを送信するだけで未提出課題の取得を行います。'
    }
    return render(request, 'linebot_api/success.html', params)