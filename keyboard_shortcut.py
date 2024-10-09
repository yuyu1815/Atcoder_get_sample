import keyboard
import threading
#キーボードショートカット
def watch_shortcut():

    def on_shortcut_1():
        keyboard.write('Hello, world!')

    def on_shortcut_2():
        keyboard.write('Hello, world!')

    def on_shortcut_3():
        keyboard.write('Hello, world!')

    def on_shortcut_4():
        keyboard.write('Hello, world!')

    def on_shortcut_5():
        keyboard.write('Hello, world!')
    keyboard.add_hotkey('ctrl+1', on_shortcut_1)
    keyboard.add_hotkey('ctrl+2', on_shortcut_2)
    keyboard.add_hotkey('ctrl+3', on_shortcut_3)
    keyboard.add_hotkey('ctrl+4', on_shortcut_4)
    keyboard.add_hotkey('ctrl+5', on_shortcut_5)
    keyboard.wait()  # プログラムが終了しないように待機

def start_shortcut_watch():
    threading.Thread(target=watch_shortcut, daemon=True).start()