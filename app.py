from flask import Flask, render_template
import pyrebase
import json

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
data1 = db.child("data").get().val()
data2 = db.child("student_info").get().val()
attend = json.loads(json.dumps(data1))
student_info = json.loads(json.dumps(data2))


@app.route('/',methods = ['POST','GET'])
def fetch_data():
    pass
    # headings = ('USN','NAME','SEM','BRANCH','SESSION 1','SESSION 2','DATE')
    # att_data = []
    # fd = attend[branch][sem][date]
    # fd_keys = fd.keys()
    # for j in fd_keys:
    #     temp = []
    #     temp.append(j)
    #     temp.append(student_info[branch][sem][j]["name"])
    #     temp.append(sem)
    #     temp.append(branch)
    #     temp.append(fd[j]['s1'])
    #     temp.append(fd[j]['s2'])
    #     temp.append(date)
    #     att_data.append(tuple(temp))

    return render_template('index.html')


# @app.route('/')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world():
#     data = db.child("data").get().val()
#     return render_template('index.html',data=data) 


# main driver function
if __name__ == '__main__':
    app.run()
