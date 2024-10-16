import re, requests
from bs4 import BeautifulSoup


def get_html_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return None
def contests(contest_id):
    html = get_html_data(f"https://atcoder.jp/contests/{contest_id}/tasks")
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
def get_url_data(url):
    html = get_html_data(url)
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

    return q_list,a_list

print(get_url_data("https://atcoder.jp/contests/agc068/tasks/agc068_a"))
