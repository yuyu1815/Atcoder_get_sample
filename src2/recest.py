
import time
import requests
import sys, re
from bs4 import BeautifulSoup
import urllib.parse
from time import sleep
import json

class Atcoder():
    def __init__(self,login_is_valid=False):
        self.login = None
        if(login_is_valid):
            self.load_login()
            self.session = self.login_session()
        else:
            self.name ,self.password = None,None


    #login save
    @staticmethod
    def save_login(name, password):
        with open("./login.json", mode="w", encoding="utf-8") as f:
            json.dump({'name':name,'password':password}, f)
    #ログインload

    def load_login(self):
        try:
            with open("./login.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            print("login.jsonが見つかりません。")
            exit()
        self.name = data['name']
        self.password = data['password']
    def login_session(self):
        login_url = "https://atcoder.jp/login"
        session = requests.session()  # sessionを作成
        res = session.get(login_url)  # cookieを取得するためにgetでアクセス
        revel_session = res.cookies.get_dict()['REVEL_SESSION']  # revel_sessionを取得
        revel_session = urllib.parse.unquote(revel_session)  # revel_sessionをデコード
        csrf_token = re.search(r'csrf_token\:(.*)_TS', revel_session).groups()[0].replace('\x00\x00',
                                                                                          '')  # csrf_tokenを正規表現で取得し、余分な文字を除去する
        sleep(1)  # 取得するまで待つ
        headers = {'content-type': 'application/x-www-form-urlencoded'}  # ヘッダーの定義
        params = {
            'username': self.name,
            'password': self.password,
            'csrf_token': csrf_token,
        }  # クエリーの定義
        data = {
            'continue': 'https://atcoder.jp/'
        }  # データの定義
        res = session.post(login_url, params=params, data=data, headers=headers)  # 必要な情報を使ってpostでログイン
        res.raise_for_status()  # http statusが異常なら例外を起こす
        return session
    def get_real_time_html_data(self, url):
        try:
            response = self.session.get(url).text
            sleep(1)
        except requests.exceptions.RequestException as e:
            print('invalid url or contest name')
            return None
        #print(f'response: {response}')
        return response
    @staticmethod
    def get_html_data(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching data: {e}")
            return None
    def contests(self,contest_id,real_time):
        if real_time:
            html = self.get_real_time_html_data(f"https://atcoder.jp/contests/{contest_id}/tasks")
        else:
            html = self.get_html_data(f"https://atcoder.jp/contests/{contest_id}/tasks")
        if html is None:
            return None, None
        # tdのclass text-center no-breakのみ取得
        soup = BeautifulSoup(html, 'html.parser')

        base_url = "https://atcoder.jp"
        questions = []
        questions_url = []
        # 各<tr>タグから問題名とURLを取得
        for row in soup.find_all('tr'):
            columns = row.find_all('a')
            if len(columns) >= 2:
                problem_name = columns[1].text
                problem_url = base_url + columns[1]['href']
                questions.append(problem_name)
                questions_url.append(problem_url)
                #print("問題文:", problem_name)
                #print("問題URL:", problem_url)
        if questions and questions_url:
            return questions, questions_url
        else:
            return None, None
    def get_url_data(self,url,real_time):
        time.sleep(0.15)
        if real_time:
            html = self.get_real_time_html_data(url)
        else:
            html = self.get_html_data(url)
        soup = BeautifulSoup(html, 'html.parser')
        div_tags = soup.find_all('div', class_='part')

        q_list = []
        a_list = []
        for div in div_tags:
            if "入力例" in div.text:
                pre_tags = div.find_all('pre')
                q_list.append(pre_tags[0].get_text())
            if  "出力例" in div.text:
                pre_tags = div.find_all('pre')
                a_list.append(pre_tags[0].get_text())
        return q_list, a_list

#print(Atcoder(True).contests("practice",True))
#print(Atcoder(True).get_real_time_html_data("https://atcoder.jp/contests/practice/tasks/practice_1"))