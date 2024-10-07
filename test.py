
import flet as ft
import re,time,json

from recest import get_html_data


def main(page: ft.Page):
    page.title = "Atcoder_sample_get"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 200  # window's width is 200 px
    page.window_height = 200  # window's height is 200 px
    page.window_resizable = False
    while True:
        dot = "..."
        for i in range(len(dot)):
            # i番目までのピリオドを取得
            page.add(ft.Text(f"コンテスト情報が読み込み中{dot[:i]}\n開始までお待ちください"))
            page.window_width = 200*i  # window's width is 200 px
            page.window_height = 200*i  # window's height is 200 px
            page.update()
            time.sleep(0.3)
            page.controls.clear()
            page.update()

ft.app(target=main)