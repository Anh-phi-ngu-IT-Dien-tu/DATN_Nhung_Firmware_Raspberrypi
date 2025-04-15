import os
import json



path = './shelves_info'
if not os.path.exists(path):
    os.mkdir(path)


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            a=file.split('.')
            print(a)