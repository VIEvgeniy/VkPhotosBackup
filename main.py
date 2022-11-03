from pprint import pprint
import YaDisk
with open('TOKEN') as token_file:
    TOKEN = token_file.readline()
DIR = 'VkPhotosBackup'
yandex_disk = YaDisk.YaDisk(TOKEN)

if __name__ == '__main__':
    yandex_disk.mkdir(DIR)
    yandex_disk.uploads(DIR, ['TOKEN'])
    pprint(yandex_disk.list())