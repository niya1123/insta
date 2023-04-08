# Tkinter, csv, seleniumライブラリをインポート
import tkinter as tk

# Tkinterのウィンドウを作る
window = tk.Tk()
window.title("Instagram Scraper")

# csvファイルを選択する関数を定義
def select_file():
    # ファイルダイアログを開く
    file = tk.filedialog.askopenfilename()
    # ファイル名をラベルに表示する
    file_label.config(text=file)

# ログインとスクレイピングを実行する関数を定義
def login_and_scrape():
    # 入力されたユーザ名とパスワードを取得する
    username = username_entry.get()
    password = password_entry.get()
    # 選択されたcsvファイル名を取得する
    file = file_label.cget("text")
    # csvファイルが選択されていない場合はエラーメッセージを表示する
    if not file:
        error_label.config(text="Please select a csv file.")
        return
    # エラーメッセージをクリアする
    error_label.config(text="")

# csvファイル選択ボタンを作る
select_button = tk.Button(window, text="Select csv file", command=select_file)
select_button.pack()

# ファイル名表示用のラベルを作る
file_label = tk.Label(window, text="")
file_label.pack()

# ユーザ名入力用のラベルとエントリーを作る
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

# パスワード入力用のラベルとエントリーを作る
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# 実行ボタンを作る
execute_button = tk.Button(window, text="Login and Scrape", command=login_and_scrape)
execute_button.pack()

error_label = tk.Label(window, text="", fg="red")
error_label.pack()

# Tkinterのウィンドウを表示する
window.mainloop()