import json

from sklearn.cluster import k_means

f = open('temp_data_file.json')
data = json.load(f)
maindata = data['data']
studinfo = data['student_info']
# print(type(data))


branch = "cse"
sem = "sem5"
date = "16-7-2022"
# session = "session1"

# headings = ('USN','NAME','SEM','BRANCH','SESSION','DATE')

att_data = []


fd = maindata[branch][sem][date]
fd_keys = fd.keys()
for j in fd_keys:
    temp = []
    temp.append(j)
    temp.append(studinfo[branch][sem][j]["name"])
    temp.append(sem)
    temp.append(branch)
    temp.append(fd[j]['s1'])
    temp.append(fd[j]['s2'])
    temp.append(date)
    att_data.append(tuple(temp))

print(att_data)
