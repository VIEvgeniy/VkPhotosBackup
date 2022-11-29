from pprint import pprint
import json
import datetime

from ProgressBar import *
import YaDisk
import VkConnect
import requests

DIR = 'VkPhotosBackup'
# vk_service_album_ids = ['wall', 'profile', 'saved']

try:
    with open('DATA') as token_file:
        DATA = json.load(token_file)
except:
    print('Файл данных DATA не найден')
    DATA = {
        'yandex_token': '',
        'vk_token': '',
        'user_id': ''
    }

yandex_disk = YaDisk.YaDisk(DATA['yandex_token'])
vk_connect = VkConnect.VkConnect(DATA['vk_token'])

while (True):
    if DATA['vk_token']:
        print('Проверка авторизации на ВКонтакте')
        user_info = vk_connect.get_user_info(1)
        if user_info:
            print('Авторизация прошла успешно')
            break
        else:
            print('Неверный токен')
            DATA['vk_token'] = ''
    else:
        while (True):
            DATA['vk_token'] = input('Введите токен ВКонтакте(ENTER - выход):')
            if not DATA['vk_token']:
                quit(1)
            if max(DATA['vk_token']) > chr(127):
                print('Недопустимые символы в токене')
            else:
                vk_connect.set_token(DATA['vk_token'])
                break

while (True):
    if DATA['user_id']:
        print('Поиск пользователя на ВКонтакте')
        user_info = vk_connect.get_user_info(DATA['user_id'])
        if user_info:
            print('Пользователь найден')
            #DATA['user_id'] = user_info['id']
            break
        else:
            print('Неверный пользователь')
            DATA['user_id'] = ''
    else:
        while (True):
            DATA['user_id'] = input('Введите id пользователя ВКонтакте(ENTER - выход):')
            if not DATA['user_id']:
                quit(2)
            if max(DATA['user_id']) > chr(127):
                print('Недопустимые символы в id пользователя')
            else:
                break

# print(f'Альбомы {DATA["user_id"]}: {vk_connect.get_albums(user_info["id"])}')

while True:
    if DATA['yandex_token']:
        print('Проверка авторизации на Яндекс Диске')
        disk_info = yandex_disk.info()
        if disk_info:
            print('Авторизация прошла успешно')
            break
        else:
            print('Неверный токен')
            DATA['yandex_token'] = ''
    else:
        while (True):
            DATA['yandex_token'] = input('Введите яндекс токен(ENTER - выход):')
            if max(DATA['yandex_token']) > chr(127):
                print('Недопустимые символы в токене')
            else:
                yandex_disk.token = DATA['yandex_token']
                break

print('Получение информации о фотографиях максимального размера')

image_list = vk_connect.get_max_photos(user_info['id'])
if image_list:
    print('Информация получена')
else:
    print('Неудалось загрузить информацию о фотографиях')
    quit(3)
# pprint(image_list)

print('Создание каталога для бэкапа на Яндекс Диске')
if yandex_disk.mkdir(f'{DIR}'):
    print('Католог создан')
else:
    print('Католог существует')

print(f'Создание каталога для бэкапа для {DATA["user_id"]} на Яндекс Диске')
if yandex_disk.mkdir(f'{DIR}/{DATA["user_id"]}'):
    print('Католог создан')
else:
    print('Католог существует')

# if not yandex_disk.mkdir(DIR):
#     quit(3)
# if yandex_disk.mkdir(DIR + '/' + DATA['user_id']):
#     print('Ok')
# else:
#     quit(4)


image_info = []

TERRA_BG = RGB(201, 100, 59, BACKGROUND)
upload_progress = ProgressBar(begin_char=FORMAT(' ', [BACKGROUND + BLUE, BOLD]),
                              body_char=FORMAT(' ', [TERRA_BG, BLUE, FRAME]),
                              end_char=FORMAT(' ', [BACKGROUND + BLUE, BOLD]),
                              space_char=FORMAT(' ', [BLUE, FRAME]))
print(f'Загрузка файлов на Яндекс диск({len(image_list)})')
index_current_file = 0
upload_progress.begin()
for image in image_list:
    filename = str(image['likes_count'])
    if image['likes_count'] in image_info:
        filename += '(' + datetime.datetime.now() + ')'
    filename += '.' + image['url'].split('.')[-1]  # '.jpg'
    filename = filename.split('?')[0]
    image_info.append({'file_name': filename, 'size': image['size_type']})
    yandex_disk.upload(f'{DIR}/{DATA["user_id"]}/{filename}', data=requests.get(image['url']))
    index_current_file += 1
    percent = (index_current_file * 100) // len(image_list)
    upload_progress.step(percent=percent, message=f'{filename}({percent}%)')
    # yandex_disk.upload_from_url(DIR + '/' + DATA["user_id"] + '/' + filename, image['url'])
upload_progress.step(percent=100)
print('Загрузка завершена')
pprint(image_info)
with open('backup_img.json', 'w') as info_file:
    info_file.write(json.dumps(image_info))
# https://disk.yandex.ru/d/lyJa_4fBqW4-ZA
