import flet as ft
import re,time,json
from activetab import start_flask
from recest import contests


class GUI:
    def __init__(self):
        self.url_text_field = None
        self.contest_name = None
        self.contest_Q_ids = []
        self.contest_Q_names = []

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
                    width=100,
                    height=100,
                    on_click=lambda _: page.go("/view3") if "https://atcoder.jp/contests/" in self.url_text_field.value else page.go("/view2") if self.url_text_field.value is None else open_dlg("URLが正しくありません")
                ),
            ])
        def sab_page():
            return ft.View("/view2", [
                ft.AppBar(title=ft.Text("コンテスト情報"),
                          bgcolor=ft.colors.RED),
                ft.Text("コンテスト情報が読み込み中...")
            ])
        def contest_window():
            self.contest_name = re.search(r"https://atcoder\.jp/contests/([^/]+)", self.url_text_field.value).group(1)
            self.contest_Q_ids, self.contest_Q_names = contests(self.contest_name)
            return ft.View("/view3", [
                ft.AppBar(title=ft.Text("コンテスト"),
                          bgcolor=ft.colors.RED),
                ft.Text(f"{self.contest_Q_ids}, {self.contest_Q_names}")
            ])
        page.title = "Atcoder_sample_get"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window_width = 500  # 幅
        page.window_height = 650  # 高さ
        # ページにビューとダイアログを追加
        page.on_route_change = route_change
        page.views.append(main_window())
        page.views.append(sab_page())
        page.overlay.append(dlg)
        page.go("/view1")



if __name__ == "__main__":
    start_flask()
    ft.app(target=GUI().start)