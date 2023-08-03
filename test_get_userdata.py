with open('userdata.csv') as f:
    for userdata in f:
        name, password = userdata.strip().split(",")
        print(name)
        print(password)