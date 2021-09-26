# normal library
import datetime
import os
import pathlib
import time

# 3rd party
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# local class
from . import bot_message_template


HOMEWORKS_TEMPALTE_PATH = 'templates/homeworks.txt'

class FailToLoginError(Exception):
    """Fail to Login Error"""
    pass


# ボタンのクリック
def button_click(browser, xpath, t=3):
    button = WebDriverWait(browser, t).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    browser.execute_script("arguments[0].click();", button)


# フォーム記入
def input_element(browser, form:dict, t=3):
    for xpath in form:
        element = WebDriverWait(browser, t).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.send_keys(form[xpath])
        time.sleep(2)


# manabaからレポート情報を取得
def scrape(id, password)-> list:
    # headlessモードで実行
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    browser.implicitly_wait(10)

    browser.get('https://ct.ritsumei.ac.jp/ct/home')
    time.sleep(1)

    # ログイン
    form_dict = {'/html/body/div/div[2]/div[1]/form/p[1]/input':id,
                '/html/body/div/div[2]/div[1]/form/p[2]/input':password}
    input_element(browser, form_dict)
    time.sleep(1)
    button_click(browser, '/html/body/div/div[2]/div[1]/form/p[3]/input')
    time.sleep(3)
    print('ログイン')
    # コース一覧へ遷移
    try:
        button_click(browser, '/html/body/div[2]/div[1]/div[6]/div[2]/a/img')
        time.sleep(1)
    except TimeoutException:
        return bot_message_template.get_template('failed_to_login.txt')

    # 受講科目の表示を曜日形式に変更
    button_click(browser, '/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[3]/a')
    time.sleep(1)

    # 授業名取得
    try:
        html = browser.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        my_courses = soup.find_all('td', attrs={'class':'course-cell'})
        my_class = []
        for course in my_courses:
            # 授業名
            course_name = course.find('a').text.split(' § ')
            name = []
            for cls_name in course_name:
                name.append(cls_name.split(':')[1])
            course_name = ' § '.join(name)
            # 課題
            homework = course.find('img', attrs={'src':'/icon-coursedeadline-on.png'})
            if homework is not None:
                my_class.append(f'{course_name}')
            else:
                my_class.append(None)
        time.sleep(1)
    except TimeoutException:
        return bot_message_template.get_template('failed_to_get_class.txt')
    
    # 課題
    found_report = False
    with open('templates/homeworks.txt', 'w') as homeworks_file:
        for inv,class_name in enumerate(my_class):
            # 未提出課題の有無を判定
            classworks = browser.find_elements_by_css_selector("div.courselistweekly-nonborder a")
            class_elem = classworks[inv*2]
            if class_name is not None:
                # 個々の授業にアクセス
                browser.execute_script("arguments[0].click();", class_elem)
                time.sleep(5)
                # レポート欄
                nonsubmit_report = browser.find_element_by_css_selector("div.course-menu-report span.my-unreadcount")
                time.sleep(5)
                if nonsubmit_report is not None:
                    found_report = True
                    course_report = browser.find_element_by_css_selector("a#coursereport")
                    browser.execute_script("arguments[0].click();", course_report)
                    time.sleep(5)
                    report_icon = browser.find_elements_by_css_selector("img[src='/icon-deadline-on.png']")
                    reports = browser.find_elements_by_css_selector("h3.report-title a")
                    deadlines = browser.find_elements_by_css_selector("td.border.center")
                    time.sleep(5)
                    for i in range(len(report_icon)):
                        deadline = deadlines[i+3].text
                        dt = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M")
                        diff = dt - now
                        homeworks_file.write('授業名:{}\nレポート名{}\n提出期限まで{}\n'.format(class_name, reports[i].text, diff))
                    time.sleep(5)
                button_click(browser, '/html/body/div[2]/div[1]/div[5]/div[2]/a/ img', 10)
                time.sleep(3)
    # 未提出課題がない
    if not found_report:
        return bot_message_template.get_template('nothing_to_submit.txt')
    return bot_message_template.get_template('homeworks.txt')

# def arrange_manaba_scrape_result(id, password):
#     message_list = manaba_scrape(id, password)
#     print(message_list)
#     messages = ""
#     if message_list[0] == "manabaのログインに失敗しました。":
#         messages = '未提出課題の課題はありません。'
#     else:
#         for i in range(len(message_list)):
#             class_name = message_list[i][0]
#             report = message_list[i][1]
#             difftime = message_list[i][2]
#             messages += f"\n授業名：{class_name}\nレポート名：{report}\n期限まで {difftime}"
#             print(messages)

#     return messages

# def create_message_template(id, password):
#     message_list = manaba_scrape(id, password)
    
        
#     template_dir_path = get_template('homeworks.txt')
