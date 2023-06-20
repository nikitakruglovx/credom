# import requests
# import json

# api_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
# params = dict(apikey='7a9fab5ff8c5f9fe92a6284d35538a9f7302179d5e1cc630fb61d60e07f98cbc')
# with open('/home/user/Desktop/Desktop.zip', 'rb') as file:
#   files = dict(file=('/home/user/Desktop/Desktop.zip', file))
#   response = requests.post(api_url, files=files, params=params)
# if response.status_code == 200:
#   result=response.json()
#   print(json.dumps(result, sort_keys=False, indent=4))

# api_url = 'https://www.virustotal.com/vtapi/v2/file/report'
# params_twos = dict(apikey='7a9fab5ff8c5f9fe92a6284d35538a9f7302179d5e1cc630fb61d60e07f98cbc', resource=str(result['resource']))
# response = requests.get(api_url, params=params_twos)
# result_two=response.json()
# print(json.dumps(result, sort_keys=False, indent=4))
# if result_two['positives'] == 0:
#     print('Вирусов не найдено')
# else:
#     print('Найдены вирусы')
#   api_url = 'https://www.virustotal.com/vtapi/v2/file/report'
#   params = dict(apikey='7a9fab5ff8c5f9fe92a6284d35538a9f7302179d5e1cc630fb61d60e07f98cbc', resource=str(result['resource']))
#   response = requests.get(api_url, params=params)
#   if response.status_code == 200:
#       result=response.json()
import os


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

file_path = 'media/media/CloudFiles/Desktop.zip'
print(file_size(file_path))