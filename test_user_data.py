import random, string
from datetime import datetime

import pandas as pd

def generate_random_string(n, used_strings):
    while True:
        random_string = ''.join(random.choices(string.ascii_letters, k=n))
        if random_string not in used_strings:
            used_strings.append(random_string)
            return random_string

lastnames = []
firstnames = []
usernames = []
passwords = []

# csvファイルの読み込み
df = pd.read_csv('userdata.csv')

for i in range(len(df)):
    used_lastnames = list(df['lastname'])
    used_firstnames = list(df['firstname'])
    used_usernames = list(df['username'])
    used_passwords = list(df['password'])
    
    lastnames.append(generate_random_string(8, used_lastnames))
    firstnames.append(generate_random_string(8, used_firstnames))
    usernames.append(generate_random_string(8, used_usernames)+''.join(random.choice(string.digits) if j == 2 else random.choice(string.ascii_letters) for j in range(8)))

    while True:
        password = generate_random_string(random.randint(8, 12), used_passwords)
        if len(password) >= 8 and len(password) <= 12:
            break
    passwords.append(password)


# 生成したランダムな文字列をデータフレームに追加してcsvファイルに保存
new_df = pd.DataFrame({'lastname': lastnames, 'firstname': firstnames, 'username': usernames, 'password': passwords})
df = pd.concat([df, new_df], ignore_index=True)
df.to_csv('userdata.csv', index=False)