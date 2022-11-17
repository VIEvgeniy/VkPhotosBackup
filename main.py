from pprint import pprint
import json
import datetime
import YaDisk
import VkConnect

DIR = 'VkPhotosBackup'

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

while(True):
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
        while(True):
            DATA['vk_token'] = input('Введите токен ВКонтакте(ENTER - выход):')
            if not DATA['vk_token']:
                quit()
            if max(DATA['vk_token']) > chr(127):
                print('Недопустимые символы в токене')
            else:
                vk_connect.token = DATA['vk_token']
                break

while(True):
    if DATA['user_id']:
        print('Поиск пользователя на ВКонтакте')
        user_info = vk_connect.get_user_info(DATA['user_id'])
        if user_info:
            print('Пользователь найден')
            break
        else:
            print('Неверный пользователь')
            DATA['vk_token'] = ''
    else:
        while(True):
            DATA['user_id'] = input('Введите id пользователя ВКонтакте(ENTER - выход):')
            if not DATA['user_id']:
                quit()
            if max(DATA['user_id']) > chr(127):
                print('Недопустимые символы в id пользователя')
            else:
                break


# while(True):
#    user_id = input('Введите id Вконтакте:')
#    if max(user_id) > chr(127):
#        print('Недопустимые символы в токене')
#        continue
#    res = vk_connect.get_user_info(user_id=user_id)
#    if not res:
#        print('Вееден не верный id')
#    else:
#        print(f'Информация о пользователе {user_id}')
#        pprint(res)
#        break


while(True):
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
        while(True):
            DATA['yandex_token'] = input('Введите яндекс токен(ENTER - выход):')
            if max(DATA['yandex_token']) > chr(127):
                print('Недопустимые символы в токене')
            else:
                yandex_disk.token = DATA['yandex_token']
                break


print('Получение информации о фотографиях максимального размера')
# user_id = res['id']
image_list = vk_connect.get_max_photos(DATA['user_id'])
if image_list:
    print('Ok')
# pprint(image_list)

print('Создание каталога для бэкапа на Яндекс Диске')
if yandex_disk.mkdir(DIR + '/' + DATA['user_id']):
    print('Ok')

image_info = []
for image in image_list:
    filename = str(image['likes_count'])
    if image['likes_count'] in image_info:
        filename += '(' + datetime.datetime.now() + ')'
    filename += '.jpg'
    image_info.append({'file_name': filename, 'size': image['size_type']})
pprint(image_info)
