import random
import string
import pandas as pd

def generate_random_string(n, used_strings: list):
    """
    list内の要素と被らないn字文字列の作成
    """
    while True:
        random_string = ''.join(random.choices(string.ascii_letters, k=n))
        if random_string not in used_strings:
            used_strings.append(random_string)
            return random_string
        
def generate_random_alias():
    length = random.randint(3, 6)
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def generate_user_data():
    emails = []
    fullnames = []
    usernames = []
    passwords = []
    userfile = 'completed_insta_user_data.csv'

    # csvファイルの読み込み
    df = pd.read_csv(userfile)
    
    
    used_emails = df['email'].tolist()
    used_fullnames = df['fullname'].tolist()
    used_usernames = df['username'].tolist()
    used_passwords = df['password'].tolist()

    alias = [s.split("+")[1].split("@")[0] for s in used_emails]
    new_alias = ''
    while True: # 無限ループ
        new_alias = generate_random_alias() # 新しい'+'以降の文字列を生成する
        if new_alias not in alias: # もし被っていなければ
            break # ループを抜ける
    
    emails.append(random.choice([p.split("+")[0] for p in used_emails]) + '+' + new_alias + '@gmail.com')
    fullnames.append(generate_random_string(8, used_fullnames))
    usernames.append(generate_random_string(8, used_usernames)+''.join(random.choice(string.digits) if j == 2 else random.choice(string.ascii_letters) for j in range(8)))
    while True:
        password = generate_random_string(random.randint(8, 12), used_passwords)
        if len(password) >= 8 and len(password) <= 12:
            break
    passwords.append(password)
    
    # 生成したランダムな文字列をデータフレームに追加してcsvファイルに保存
    save_user_data(df, pd.DataFrame({'email': emails, 'fullname': fullnames, 'username': usernames, 'password': passwords}), userfile)

    return emails[0], fullnames[0], usernames[0], passwords[0]

def save_user_data(df, new_df, filename):
    save_df = pd.concat([df, new_df], ignore_index=True)
    save_df.to_csv(filename, index=False)