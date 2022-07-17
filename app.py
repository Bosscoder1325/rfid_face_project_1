from flask import Flask, render_template, request, redirect, url_for
import pyrebase
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

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

session = False
print("global session id", id(session))
cid = ""

# config = {
#     "apiKey": "AIzaSyCc0veJ4Kez3iLS8U-qjxhOMFwnzA7WZ7U",
#     "authDomain": "fir-46336.firebaseapp.com",
#     "databaseURL": "https://fir-46336-default-rtdb.asia-southeast1.firebasedatabase.app",
#     "projectId": "fir-46336",
#     "storageBucket": "fir-46336.appspot.com",
#     "messagingSenderId": "1021317922890",
#     "appId": "1:1021317922890:web:71550b203e9eb04f8de6b3",
#     "measurementId": "G-RGCMC81BWC"
# }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
# data1 = db.child("data").get().val()
# data2 = db.child("student_info").get().val()
# attend = json.loads(json.dumps(data1))
# student_info = json.loads(json.dumps(data2))


@app.route('/edit_student', methods=['POST', 'GET'])
def edit_student():
    if request.method == 'POST':
        current_data = request.form.get('data').replace(
            "(", "").replace(")", "").split(',')
        current_data = [i.replace("'", "").strip() for i in current_data]
        current_keys = ('usn', 'name', 'sem', 'branch', 's1', 's2', 'date')
        current_dic = {}
        print("this is data got", current_data)
        print(len(current_data), len(current_keys))
        for i in range(len(current_data)):
            current_dic.update({current_keys[i]: current_data[i]})
        print("curretn dic", current_dic)

    return render_template('edit_student.html', data=current_dic)
    # return render_template('edit_student.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    global session
    session = False
    return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def fetch_data():
    if session:
        data1 = db.child("data").get().val()
        data2 = db.child("student_info").get().val()
        attend = json.loads(json.dumps(data1))
        student_info = json.loads(json.dumps(data2))

        branch = sem = date = ""
        att_data = []
        headings = ('USN', 'NAME', 'SEM', 'BRANCH',
                    'SESSION 1', 'SESSION 2', 'DATE', 'EDIT', 'DELETE')
        if request.method == "POST":
            # getting input with name = fname in HTML form
            branch = request.form.get("branch")
            sem = request.form.get("sem")
            date = request.form.get("date")

            print(branch, sem, date)

            fd = attend[branch][sem][date]
            fd_keys = fd.keys()
            for j in fd_keys:
                temp = []
                temp.append(j)
                temp.append(student_info[branch][sem][j]["name"])
                temp.append(sem)
                temp.append(branch)
                temp.append(fd[j]['s1'])
                temp.append(fd[j]['s2'])
                temp.append(date)
                att_data.append(tuple(temp))

        return render_template('index.html', headings=headings, rows=att_data)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    data = db.child("creds").get().val()
    creds = json.loads(json.dumps(data))
    if request.method == 'POST':
        cid = request.form.get('uname')
        passw = request.form.get('pass')
        if cid in creds.keys():
            if passw == creds[cid]:
                global session
                session = True
                print("internal session id", id(session))
                print("session started", session)
                return redirect('/')
            else:
                print("check your creds")
        else:
            print('user not found')
    else:
        print("not working")
    return render_template('login.html')


@app.route('/edited', methods=['POST', 'GET'])
def edited():
    data1 = db.child("data").get().val()
    data2 = db.child("student_info").get().val()
    attend = json.loads(json.dumps(data1))
    student_info = json.loads(json.dumps(data2))

    headings = ('USN', 'NAME', 'SEM', 'BRANCH',
                'SESSION 1', 'SESSION 2', 'DATE', 'EDIT', 'DELETE')
    usn = name = sem = branch = s1 = s2 = ""
    if request.method == 'POST':
        all_data = request.form.get("all_data")

        data = [i.strip() for i in all_data.strip().replace(
            "{", "").replace("}", "").replace("'", "").split(",")]

        for i in data:
            if i.startswith('branch'):
                temp = i.strip().split(":")
                branch = temp[1].strip()
            elif i.startswith('sem'):
                temp = i.strip().split(":")
                sem = temp[1].strip()
            elif i.startswith('usn'):
                temp = i.strip().split(":")
                usn = temp[1].strip()
            elif i.startswith('date'):
                temp = i.strip().split(":")
                date = temp[1].strip()

            s1 = request.form.get('s1')
            s2 = request.form.get('s2')

    # all_data_dic me ye mila
    # {'usn': '1kt18cs004', 'name': 'Diwan', 'sem': 'sem5',
    #     'branch': 'cse', 's1': 'True', 's2': 'True', 'date': '16-7-2022'}

    attend[branch][sem][date][usn]['s1'] = s1
    attend[branch][sem][date][usn]['s2'] = s2

    db.child('data').update(attend)
    print(usn, name, sem, branch)
    return redirect('/')


@app.route('/delete', methods=['POST', 'GET'])
def delete_data():
    data1 = db.child("data").get().val()
    data2 = db.child("student_info").get().val()
    attend = json.loads(json.dumps(data1))
    student_info = json.loads(json.dumps(data2))

    current_data = request.form.get('data').replace(
        "(", "").replace(")", "").split(',')
    current_data = [i.replace("'", "").strip() for i in current_data]
    current_keys = ('usn', 'name', 'sem', 'branch', 's1', 's2', 'date')
    current_dic = {}
    print("this is data got", current_data)
    print(len(current_data), len(current_keys))
    for i in range(len(current_data)):
        current_dic.update({current_keys[i]: current_data[i]})
    print("curretn dic", current_dic)

    # all_data_dic me ye mila
    # {'usn': '1kt18cs004', 'name': 'Diwan', 'sem': 'sem5',
    #     'branch': 'cse', 's1': 'True', 's2': 'True', 'date': '16-7-2022'}
    print(type(current_dic))
    branch = current_dic["branch"]
    sem = current_dic["sem"]
    date = current_dic["date"]
    usn = current_dic["usn"]
    del attend[branch][sem][date][usn]
    db.child('data').update(attend)
    return redirect('/')

# @app.route('/')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world():
#     return render_template('index.html')


@app.route('/analysis', methods=['POST', 'GET'])
def analyze_data():
    branch = sem = date = ""
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    data1 = db.child("data").get().val()
    data2 = db.child("student_info").get().val()
    attend = json.loads(json.dumps(data1))
    student_info = json.loads(json.dumps(data2))

    if request.method == "POST":
        # getting input with name = fname in HTML form
        branch = request.form.get("branch")
        sem = request.form.get("sem")
        date = request.form.get("date")

        dates = attend[branch][sem].keys()
        s1 = 0
        main_list = []
        for i in dates:
            temp_dic = {}
            usn = attend[branch][sem][i].keys()
            for j in usn:
                if attend[branch][sem][i][j]['s1'] == True:
                    if 's1' not in temp_dic.keys():
                        temp_dic.update({"date": i, 's1': 1, })
                    else:
                        temp_dic['s1'] += 1
                if attend[branch][sem][i][j]['s2'] == True:
                    if 's2' not in temp_dic.keys():
                        temp_dic.update({"date": i, 's2': 1})
                    else:
                        temp_dic['s2'] += 1
            main_list.append(temp_dic)

        df = pd.DataFrame(main_list)
        # date:date, s1:count, s2:count
        fig = px.bar(df, x="date", y=["s1", "s2"])
        fig.write_image("static/img/ses.png")

    return render_template("analyze_all_student.html")


# main driver function
if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=50000, debug=True)
