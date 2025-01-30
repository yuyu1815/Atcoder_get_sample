import flet as ft
import re
import pyperclip
import recest
import sys

class GUI:
    def __init__(self):
        self.real_time = False
        self.url_text_field = None
        self.contest_name = None
        self.contest_Q_urls = []
        self.contest_Q_names = []
        self.request_data = None
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
                ft.Switch(
                    label="リアルタイム",
                    on_change=lambda e: setattr(self, 'real_time', not self.real_time),
                    value=self.real_time,
                ),
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
                    self.request_data = recest.Atcoder(self.real_time)
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
                self.contest_Q_names, self.contest_Q_urls = self.request_data.contests(self.contest_name,self.real_time)
                print(self.contest_Q_names,self.contest_Q_urls)
                # タブの作成
                tabs_data = []
                # 各タブの内容を格納するリスト
                tab_contents = []
                for contest_Q_url, contest_Q_name in zip(self.contest_Q_urls, self.contest_Q_names):
                    questions, answers = self.request_data.get_url_data(contest_Q_url, self.real_time)
                    if questions is None or answers is None:
                        continue
                    contents = ""
                    for question, answer in zip(questions, answers):
                        contents += f"case\n\n{question}\nanswer\n\n{answer}\n"

                    # タブの内容をリストに追加
                    tab_contents.append(contents)

                    # コピーボタンを含むヘッダー部分
                    header = ft.Container(
                        content=ft.ElevatedButton(
                            text="すべてをコピー",
                            on_click=lambda e, index=len(tab_contents) - 1: pyperclip.copy(tab_contents[index]),
                        ),
                        margin=ft.margin.only(bottom=10)
                    )

                    # スクロール可能なテキストコンテンツ
                    scrollable_text = ft.Container(
                        content=ft.Text(contents),
                        padding=10,
                        height=350,  # スクロール領域の高さを調整
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=8
                    )

                    tab = ft.Tab(
                        text=contest_Q_name,
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    header,  # コピーボタンを最上部に配置
                                    scrollable_text  # スクロール可能なテキスト領域
                                ],
                                #scroll=ft.ScrollMode.NONE,  # メインのColumnではスクロールを無効化
                                expand=True,
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
                            content=tabs_view,
                            padding=10,
                            border=ft.border.all(1),
                            expand=True  # コンテナも拡張
                        )
                    ]
                )
            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_no = exception_traceback.tb_lineno
                print(f"{filename}の{line_no}行目でエラーが発生しました。詳細：{e}")
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
        self.contest_Q_names, self.contest_Q_urls = self.request_data.contests(self.contest_name,self.real_time)

        # タブの作成
        tabs_data = []
        key_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z"]
        for i in range(len(self.contest_Q_names)):
            questions, answers = self.request_data.get_url_data(self.contest_Q_urls[i],self.real_time)
            with open(f"./out/{key_list[i]}.txt", mode="w", encoding="utf-8") as f:  # 拡張子を変更
                for question, answer in zip(questions, answers):
                    # 改行を整理
                    question_cleaned = "\n".join(line.strip() for line in question.splitlines() if line.strip())
                    answer_cleaned = "\n".join(line.strip() for line in answer.splitlines() if line.strip())
                    f.write(f"case\n{question_cleaned}\nanswer\n{answer_cleaned}\n")


if __name__ == "__main__":
    #start_flask()
    ft.app(target=GUI().start)