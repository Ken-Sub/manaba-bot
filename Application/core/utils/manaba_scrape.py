# 3rd party
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# normal library
import time
import datetime

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
def manaba_scrape(id, password)-> list:
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

    # コース一覧へ遷移
    try:
        button_click(browser, '/html/body/div[2]/div[1]/div[5]/div[2]/a/img')
        time.sleep(1)
    except:
        error_message = ['manabaのログインに失敗しました。']
        browser.quit()
        return error_message

    # 受講科目の表示を曜日形式に変更
    button_click(browser, '/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[3]/a')
    time.sleep(1)

    # 授業名取得
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
   
    # 課題
    report_and_difftime = []
    for inv,class_name in enumerate(my_class):
        # 未提出課題の有無を判定
        classworks = browser.find_elements_by_css_selector("div.courselistweekly-nonborder a")
        class_elem = classworks[inv*2]
        if class_name is not None:
            # 個々の授業にアクセス
            browser.execute_script("arguments[0].click();", class_elem)
            time.sleep(1)
            # レポート欄
            nonsubmit_report = browser.find_element_by_css_selector("div.course-menu-report span.my-unreadcount")
            time.sleep(1)
            if nonsubmit_report is not None:
                course_report = browser.find_element_by_css_selector("a#coursereport")
                browser.execute_script("arguments[0].click();", course_report)
                time.sleep(1)
                report_icon = browser.find_elements_by_css_selector("img[src='/icon-deadline-on.png']")
                reports = browser.find_elements_by_css_selector("h3.report-title a")
                deadlines = browser.find_elements_by_css_selector("td.border.center")
                time.sleep(1)
                for i in range(len(report_icon)):
                    deadline = deadlines[i+3].text
                    dt = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M")
                    diff = dt - now
                    report_info = (class_name,reports[i].text,diff)
                    report_and_difftime.append(report_info)
                time.sleep(1)
            button_click(browser, '/html/body/div[2]/div[1]/div[5]/div[2]/a/img', 10)
            time.sleep(3)
    return report_and_difftime

def arrange_manaba_scrape_result(id, password):
    message_list = manaba_scrape(id, password)
    print(message_list)
    messages = ""
    if message_list[0] == "manabaのログインに失敗しました。":
        messages = '未提出課題の課題はありません。'
    else:
        for i in range(len(message_list)):
            class_name = message_list[i][0]
            report = message_list[i][1]
            difftime = message_list[i][2]
            messages += f"\n授業名：{class_name}\nレポート名：{report}\n期限まで {difftime}"
            print(messages)

    return messages
