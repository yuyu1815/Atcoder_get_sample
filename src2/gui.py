import flet as ft
import re,time,json

import pyperclip

from activetab import start_flask
from recest import contests, get_url_data


class GUI:
    def __init__(self):
        self.url_text_field = None
        self.contest_name = None
        self.contest_Q_urls = []
        self.contest_Q_names = []

        self.download_button = False

    def start(self, page: ft.Page):
        # error閉じる
        def close_dlg(e):
            dlg.open = False
            page.update()
        #error
        def open_dlg(msg):
            dlg.content = ft.Text(msg)
            dlg.open = True
            page.update()

        def route_change(handler):
            troute = ft.TemplateRoute(handler.route)
            if troute.match("/view1"):
                page.views.append(main_window())
            if troute.match("/view1_download"):
                page.views.append(main_window())
            elif troute.match("/view2"):
                page.views.append(sab_page())
            elif troute.match("/view3"):
                page.views.append(contest_window())
            page.update()
        # ダイアログの定義
        dlg = ft.AlertDialog(
            title=ft.Text("エラー"),
            modal=True,
            content=ft.Text(""),
            actions=[
                ft.TextButton("閉じる", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # メインページ
        def main_window():
            self.url_text_field = ft.TextField(label="実行するURLを入れてください(なくても動きます)")
            return ft.View("/view1", [
                ft.AppBar(title=ft.Text("Menu"), bgcolor=ft.colors.RED),
                self.url_text_field,
                ft.ElevatedButton(
                    text="▶",
                    width=60,
                    height=60,
                    on_click=lambda _: goto_page()
                ),
                ft.ElevatedButton(
                    text="ダウンロード",
                    width=150,
                    height=50,
                    on_click= lambda _: self.all_download()
                )
            ])
        def goto_page():
            if("https://atcoder.jp/contests/" in self.url_text_field.value):
                if self.download_button:
                    page.go("/view1_download")
                else:
                    page.go("/view3")
            elif(self.url_text_field.value is None):
                page.go("/view2")
            else:
                open_dlg("URLが正しくありません")
        def sab_page():
            return ft.View("/view2", [
                ft.AppBar(title=ft.Text("コンテスト情報"),
                          bgcolor=ft.colors.RED),
                ft.Text("コンテスト情報が読み込み中...")
            ])

        def contest_window():
            try:
                # URLからコンテスト名を取得
                self.contest_name = re.search(r"https://atcoder\.jp/contests/([^/]+)", self.url_text_field.value).group(
                    1)
                self.contest_Q_names, self.contest_Q_urls = contests(self.contest_name)

                # タブの作成
                tabs_data = []
                for contest_Q_url, contest_Q_name in zip(self.contest_Q_urls, self.contest_Q_names):
                    questions, answers = get_url_data(contest_Q_url)
                    contents = ""
                    for question, answer in zip(questions, answers):
                        contents += f"case\n\n{question}\nanswer\n\n{answer}\n"

                    # スクロール可能なコンテナを作成
                    scrollable_content = ft.Container(
                        content=ft.Column([
                            ft.Text(contents)
                        ]),
                        padding=10,
                        height=400,  # コンテナの高さを固定
                        expand=True  # 利用可能なスペースいっぱいに広がる
                    )

                    tab = ft.Tab(
                        text=contest_Q_name,
                        content=ft.Container(
                            content=ft.Column(
                                [scrollable_content],
                                scroll=ft.ScrollMode.ALWAYS,  # スクロールを有効化
                                expand=True,  # 利用可能なスペースいっぱいに広がる
                                spacing=10
                            ),
                            padding=10
                        )
                    )
                    tabs_data.append(tab)

                # タブビューの作成
                tabs_view = ft.Tabs(
                    selected_index=0,
                    tabs=tabs_data,
                    expand=True  # タブビューも拡張
                )

                # メインコンテンツの作成
                main_content = ft.Column([
                    tabs_view,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="すべてをコピー",
                            on_click=lambda e, pre_text=contents: pyperclip.copy(pre_text),
                        ),
                        margin=ft.margin.only(top=10)
                    )
                ], expand=True)  # メインコンテンツも拡張

                return ft.View(
                    "/view3",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/view1")
                            ),
                            title=ft.Text("コンテスト"),
                            bgcolor=ft.colors.RED
                        ),
                        ft.Container(
                            content=main_content,
                            padding=10,
                            border=ft.border.all(1),
                            expand=True  # コンテナも拡張
                        )
                    ]
                )
            except Exception as e:
                print(f"Error in contest_window: {str(e)}")
                return ft.View(
                    "/view3",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/view1")
                            ),
                            title=ft.Text("エラー"),
                            bgcolor=ft.colors.RED
                        ),
                        ft.Text(f"エラーが発生しました: {str(e)}")
                    ]
                )
        page.title = "Atcoder_sample_get"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.width = 500  # 幅
        page.window.height = 650  # 高さ
        # ページにビューとダイアログを追加
        page.on_route_change = route_change
        page.views.append(main_window())
        page.views.append(sab_page())
        page.overlay.append(dlg)
        page.go("/view1")

    def all_download(self):
        # URLからコンテスト名を取得
        match = re.search(r"https://atcoder\.jp/contests/([^/]+)", self.url_text_field.value)
        if match is None:
            print("エラー: URLが無効です。")
            return  # または適切なエラーメッセージを表示する

        self.contest_name = match.group(1)
        self.contest_Q_names, self.contest_Q_urls = contests(self.contest_name)

        # タブの作成
        tabs_data = []
        key_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z"]
        for i in range(len(self.contest_Q_names)):
            questions, answers = get_url_data(self.contest_Q_urls[i])
            with open(f"./out/{key_list[i]}.txt", mode="w", encoding="utf-8") as f:  # 拡張子を変更
                for question, answer in zip(questions, answers):
                    # 改行を整理
                    question_cleaned = "\n".join(line.strip() for line in question.splitlines() if line.strip())
                    answer_cleaned = "\n".join(line.strip() for line in answer.splitlines() if line.strip())
                    f.write(f"case\n{question_cleaned}\nanswer\n{answer_cleaned}\n")


if __name__ == "__main__":
    #start_flask()
    ft.app(target=GUI().start)
