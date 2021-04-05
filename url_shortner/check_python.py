import os
import json
urls={}
if os.path.exists('url_file.json'):
    with open('url_file.json','r') as file:
        urls=json.load(file)
print(urls.keys())
print(urls.values())
