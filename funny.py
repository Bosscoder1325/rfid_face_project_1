from flask import Flask, render_template, request, redirect
import pyrebase
import json
config = {
    "apiKey": "AIzaSyAZoAADcMtseOtxeAh6jLcpH3or24ZhL8c",
    "authDomain": "rfid-aaea6.firebaseapp.com",
    "databaseURL": "https://rfid-aaea6-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "rfid-aaea6",
    "storageBucket": "rfid-aaea6.appspot.com",
    "messagingSenderId": "621829893183",
    "appId": "1:621829893183:web:e04119660c08c0c44a1c8a",
    "measurementId": "G-3GT9ED7KXE"
}
# from sklearn.cluster import k_means

# f = open('temp_data_file.json')
# data = json.load(f)
# maindata = data['data']
# studinfo = data['student_info']
# # print(type(data))


# branch = "cse"
# sem = "sem5"
# date = "16-7-2022"
# # session = "session1"

# # headings = ('USN','NAME','SEM','BRANCH','SESSION','DATE')

# att_data = []


# fd = maindata[branch][sem][date]
# fd_keys = fd.keys()
# for j in fd_keys:
#     temp = []
#     temp.append(j)
#     temp.append(studinfo[branch][sem][j]["name"])
#     temp.append(sem)
#     temp.append(branch)
#     temp.append(fd[j]['s1'])
#     temp.append(fd[j]['s2'])
#     temp.append(date)
# #     att_data.append(tuple(temp))

# data = ('1kt18cs004', 'Diwan', 'sem5', 'cse', False, True, '16-7-2022')
# current_keys = ('usn', 'name', 'sem', 'branch', 's1', 's2', 'date')
# current_dic = {}
# for i in range(len(current_data)):
#     current_dic.update({current_keys[i]: current_data[i]})

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
# data1 = db.child("data").get().val()
# data2 = db.child("student_info").get().val()
# attend = json.loads(json.dumps(data1))
# student_info = json.loads(json.dumps(data2))
# print(attend)
# usn = '1kt18cs004'
# # name = request.form.get('name')
# sem = 'sem5'
# branch = 'cse'
# s1 = True
# s2 = True
# date = '16-7-2022'

# attend[branch][sem][date][usn]['s1'] = s1
# attend[branch][sem][date][usn]['s2'] = s2
# db.child('data').update(attend)


data = [i.strip() for i in "{'usn': '1kt18cs004', 'name': 'Diwan', 'sem': 'sem5', 'branch': 'cse', 's1': 'True', 's2': 'True', 'date': '16-7-2022'}".strip().replace("{","").replace("}", "").replace("'", "").split(",")]

# data = [i.split(":") for i in data]

for i in data:
    if i.startswith('branch'):
        temp = i.strip().split(":")
        print(temp[1])

# print(data)
