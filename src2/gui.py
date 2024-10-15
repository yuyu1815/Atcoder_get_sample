import flet as ft

from activetab import start_flask


class GUI:
    def __init__(self):
        self.url_text_field = None

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
                    on_click=lambda _: page.go("/view2") if "https://atcoder.jp/contests/a" in self.url_text_field.value else open_dlg("URLが正しくありません")
                ),
            ])

        def sab_page():
            return ft.View("/view2", [
                ft.AppBar(title=ft.Text("コンテスト情報"),
                          bgcolor=ft.colors.RED),
                ft.Text("コンテスト情報が読み込み中...")
            ])
        page.title = "Atcoder_sample_get"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window_width = 500  # 幅
        page.window_height = 650  # 高さ
        # ページにビューとダイアログを追加
        #page.views.append(sab_page())
        page.views.append(main_window())
        page.overlay.append(dlg)
        page.update()
        page.go("/view1")



if __name__ == "__main__":
    start_flask()
    ft.app(target=GUI().start)