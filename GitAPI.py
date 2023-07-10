#!/usr/bin/python3

import json
import requests
import time
import csv
import re
import datetime
from requests.auth import HTTPBasicAuth

author = "verdaccio"
repositry = "verdaccio"
author = "contentful"
repositry = "the-example-app.nodejs"

commit_date = []
commit_file = ["DATA"]
commit_oneday = []

page = 1
authorization = "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"
print("☠ Data collection phase start ☠")

while(True):
    #git_url = "https://api.github.com/repos/" + author + "/" + repositry + "/commits?page=" + str(page) + "&per_page=2"
    git_url = "https://api.github.com/repos/" + author + "/" + repositry + "/commits?page=" + str(page)
    print(git_url)
    response_1 = requests.get(git_url, auth=HTTPBasicAuth('C0A20028',authorization))
    data_list = json.loads(response_1.text)
    if(len(data_list)==0):
        break

    for i in range(len(data_list)):
        url = data_list[i]["url"]
        response_2 = requests.get(url, auth=HTTPBasicAuth('C0A20028',authorization))
        data_file = json.loads(response_2.text)

        try:
            date = data_file["commit"]["author"]["date"]
            date = re.search('\d+-\d+-\d+',date)
            date = date.group()
            date = date[2:]
            date = date.replace('-','_')
            print(date)
            for j in range(len(data_file["files"])):
                filename = data_file["files"][j]["filename"]
                if(date not in commit_date):
                    commit_oneday.append([0 for _ in range(len(commit_file))])
                    commit_date.append(date)
                if(filename not in commit_file):
                    commit_file.append(filename)
                    commit_oneday[len(commit_oneday)-1].append(1)
                else:
                    commit_oneday[len(commit_oneday)-1][commit_file.index(filename)] += 1
                print(filename)
            time.sleep(7)
            
           
        except:
            print("NO DATA")
            time.sleep(7)
            continue
    page += 1

print("☠ Data collection phase completed ☠")

print("☠ write csv phase start ☠")

commit_csv = []
commit_csv.append(commit_date)

for i in range(len(commit_file)):
    if(i==0):
        continue
    commit_csv.append([commit_file[i]])

for i in range(len(commit_date)):
    for j in range(len(commit_file)):
        if(j==0):
            continue
        if(j < len(commit_oneday[i])):
            commit_csv[j].append(commit_oneday[i][j])
        else:
            commit_csv[j].append(0)

commit_date.reverse()
commit_date.insert(0,"")
#commit_oneday.reverse()

with open('./Github_' + repositry + '_history.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(commit_csv)

print("☠ write csv phase completed ☠")