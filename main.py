# from pprint import pprint
import json
# import YaDisk
import VkConnect

with open('TOKEN') as token_file:
     TOKEN = json.load(token_file)
# DIR = 'VkPhotosBackup'
# pprint(TOKEN)
# yandex_disk = YaDisk.YaDisk(TOKEN['yandex_token'])
import requests

req = "https://api.vk.com/method/users.get?user_ids=210700286&fields=bdate&access_token="+TOKEN['vk_token']+"&v=5.131"
if __name__ == '__main__':
#    yandex_disk.mkdir(DIR)
#    yandex_disk.uploads(DIR, ['TOKEN'])
#    pprint(yandex_disk.list())
    res = requests.get(req)
    print(res.json())