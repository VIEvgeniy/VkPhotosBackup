from pprint import pprint
import json
# import YaDisk
from VkConnect import VkConnect as VkConn

with open('TOKEN') as token_file:
    TOKEN = json.load(token_file)
# DIR = 'VkPhotosBackup'
# pprint(TOKEN)
# yandex_disk = YaDisk.YaDisk(TOKEN['yandex_token'])

vk_connect = VkConn(TOKEN['vk_token'])

if __name__ == '__main__':
    #    yandex_disk.mkdir(DIR)
    #    yandex_disk.uploads(DIR, ['TOKEN'])
    #    pprint(yandex_disk.list())

    #    res = requests.get(req)
    #    print(res.json())

    res = vk_connect.get_user_info(user_id='655463')
    user_id = res['id']
    res = vk_connect.get_max_photos(user_id)
    pprint(res)
