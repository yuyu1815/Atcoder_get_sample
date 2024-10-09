from turtledemo.paint import switchupdown
import pyperclip
import flet as ft
import re,time,json
import activetab
from recest import contests, get_url_data


page_active_bool = False
msg_hint_bool = False
def main(page: ft.Page):
    page.title = "Atcoder_sample_get"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 500  # 幅
    page.window_height = 600  # 高さ
    name_input = ft.TextField(label="実行するURLを入れてください(なくても動きます)")

    def on_play_button_click(e):
        sab_page(name_input.value, page)

    # 再生ボタンを作成
    play_button = ft.ElevatedButton(
        text="開始",
        width=100,
        height=100,
        on_click=on_play_button_click
    )
    with open("qiita_write.json", mode="w", encoding="utf-8") as f:
        json.dump("", f)
    # ページにボタンを追加
    page.add(name_input, play_button)
def page_clean(page: ft.Page):
    page.controls.clear()
    page.update()
def sab_page(url, page: ft.Page):
    def contest_cancel_button_click(e):
        page.controls.clear()
        page.window.close()
    # サーバー
    activetab.start_flask()
    # ページをクリア
    page.controls.clear()
    if "https://atcoder.jp/contests/" in url :
        # パターンに一致する部分を検索
        match = re.search(r"https://atcoder\.jp/contests/([^/]+)", url).group(1)
        # 新たな内容を追加
        page.add(ft.Text(f"新しいページが生成されました。URL: {match}"))
        page.update()
    else:
        dot = ""
        while True:
            load_url = activetab.get_url_status()
            page.add(ft.Text(f"URLなしモードで実行します{dot}\nブラウザからurlを取得しています"))
            page_clean(page)
            time.sleep(0.3)
            if len(dot) < 3:
                dot += "."
            else:
                dot = ""
            # 何かはあった
            re_load_url = []
            if load_url:
                for url in load_url:
                    if "https://atcoder.jp/contests/" != url[0] and "https://atcoder.jp/?lang" not in url[0] and "https://atcoder.jp/" != url[0] and "https://atcoder.jp/home" != url[0]:
                        re_load_url.append(url)
            if re_load_url:
                page.add(ft.Text(f"URLが読み込まれました。URL: {load_url[0][0]}"))
                page.update()
                time.sleep(2)
                page_clean(page)
                break
        for item in load_url:
            #1この場合
            if len(load_url) == 1:
                url = item[0]
                break
            #複数個ある場合ブラウザの開いている画面から優先
            if "https://atcoder.jp/contests/" in item and item[1]:
                url = item[0]
                break
        else:
            url = load_url[0][0]
    while True:
        # ローディング
        dot = "..."
        for i in range(len(dot)):
            # i番目までのピリオドを取得
            page.add(ft.Text(f"コンテスト情報が読み込み中{dot[:i]}\n開始までお待ちください"),ft.ElevatedButton(text="キャンセル",on_click=contest_cancel_button_click))
            page.update()
            time.sleep(0.3)
            page_clean(page)
        try:
            match = re.search(r"https://atcoder\.jp/contests/([^/]+)", url).group(1)
        except:
            continue
        contest_loader(page, match)
        load_url = activetab.get_url_status()
        re_load_url = []
        if load_url:
            for url in load_url:
                if "https://atcoder.jp/contests/" != url[0] and "https://atcoder.jp/?lang" not in url[0] and "https://atcoder.jp/" != url[0] and "https://atcoder.jp/home" != url[0]:
                    re_load_url.append(url)
        
def contest_loader(page,content_id):
    # curl
    questions, questions_url = contests(content_id)
    print(questions,questions_url)
    if not(questions or questions_url) :
        return None
    #ページクリアー
    page_clean(page)
    #上のタブ部分
    def on_tab():
        page.add(ft.Column(controls=[ft.Container(content=tabs,width=500,height=50,)],expand=True ))
    #設定
    def active_tab_change(event):
        global page_active_bool
        page_active_bool = event.control.value
        page.window.always_on_top = page_active_bool # 画面を固定するかどうか
    #設定2
    def msg_hint_change(event):
        global msg_hint_bool
        msg_hint_bool = event.control.value

    def _tab(active_tab):
        global page_active_bool, msg_hint_bool
        page_clean(page)
        on_tab()
        match active_tab:
            case 0:
                print("設定")
                page.add( ft.Switch(label="画面を固定",on_change=active_tab_change, value=page_active_bool))  # Switchの作成
                page.add( ft.Switch(label="例1のを表示",on_change=msg_hint_change, value=msg_hint_bool))  # Switchの作成
            case _:
                active_tab_element(active_tab)

        page.update()
    def example_question(pre_text):

        print("例を表示します")
    def active_tab_element(active_tab):
        print(questions[active_tab - 1])
        html_elements = get_url_data(questions_url[active_tab - 1])
        controls = []
        elevate1_button = []
        elevate2_button = []

        for element in html_elements:
            controls.append(ft.Container(
                ft.Column([
                    ft.Text(f"{element['h3'][0]}\n{element['pre'][0]}"),

                ]),
                key=element['h3'][0]
            ))
        for element in html_elements:
            if "入力例" in element['h3'][0]:
                elevate1_button.append(
                    ft.ElevatedButton(
                        text=element['h3'][0],
                        on_click=lambda e, pre_text=element['h3'][0]:cl.scroll_to(key=pre_text, duration=1000),
                    )
                )
                #クリップボードコピー
                elevate2_button.append(
                    ft.ElevatedButton(
                        text=element['h3'][0],
                        on_click=lambda e, pre_text=element['pre'][0]: pyperclip.copy(pre_text),
                    )
                )

        cl = ft.Column(
            spacing=10,
            height=300,
            width=500,
            scroll=ft.ScrollMode.ALWAYS,
            controls=controls,
        )

        page.add(
            ft.Container(cl, border=ft.border.all(1)),
            ft.Column([ft.Text("例を表示:"), ft.Row(elevate1_button)]),
            ft.Column([ft.Text("例をコピー:"), ft.Row(elevate2_button)]),
        )

    def on_tab_change(e):
        _tab(tabs.selected_index)

    tabs_item = []
    tabs_item.append(ft.Tab(text=f"0：設定"))
    for i in range(len(questions)):
        # 新しいタブを追加
        tabs = tabs_item.append(ft.Tab(text=f"{i+1}：{questions[i]}"))
    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_tab_change,
        tabs=tabs_item
    )

    # タブを上部に配置
    _tab(tabs.selected_index)
    #on_tab()
    page.update()
    old_url = questions_url[0]
    now_url = None
    while True:
        active_tab = False
        time.sleep(3)
        urls = activetab.get_url_status()
        # 現在のタブが更新されていたら更新

        if urls is None:
            break
        for i in range(len(urls)):
            if urls[i][1]:
                active_tab = True
                now_url = urls[i][0]
                break
        if not active_tab:
            for i in range(len(urls)):
                if "tasks/" in urls[i][0]:
                    now_url = urls[i][0]
                    break
        if  now_url is None:
            continue
        if "tasks/" in now_url:
            match_old = re.search(r"https://atcoder\.jp/contests/([^/]+)/tasks/([^/]+)", old_url)
            match_new = re.search(r"https://atcoder\.jp/contests/([^/]+)/tasks/([^/]+)", now_url)
        elif "contests/":
            continue
        else:
            break
        # 現在のコンテストが更新されていたら更新
        if match_old.group(1) != match_new.group(1):
          break
        # 現在のタスクが更新されていたら更新
        else:
            for i in range(len(questions_url)):
                if match_new.group(2) in questions_url[i] and tabs.selected_index != i+1:
                    tabs.selected_index = i+1
                    page.update()
                    _tab(i+1)
                    break
            old_url = now_url

# アプリを実行
ft.app(target=main)
