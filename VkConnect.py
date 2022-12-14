import requests


class VkConnect:
    def __init__(self, token='', version='5.131'):
#        self.token = token
        self.host = 'https://api.vk.com/method/'
#        self.version = version
        self.params = {'access_token': token, 'v': version}
    def set_token(self, token):
        self.params['access_token'] = token
    def _get_api_url(self, api=''):
        res = f'{self.host}{api}'
        return res

    def get_user_info(self, user_id, fields=''):
        params = {'user_id': user_id, 'fields': fields}
        res = requests.get(self._get_api_url('users.get'), params={**self.params, **params}).json()
        if 'response' in res and len(res['response']):
            return res['response'][0]

    def get_max_photos(self, user_id, album_id='profile', count=5):
        params = {'owner_id': user_id, 'album_id': album_id, 'count': count, 'extended': '1'}
        res = requests.get(self._get_api_url('photos.get'), params={**self.params, **params}).json()
        if 'error' in res:
            return []
        res = res['response']
        images_info = []
        # s - 75px, o - 130px, m - 130px, p - 200px, q - 320px, r - 510px, y - 807px, z - 1024px, w - 2048px
        # взято от сюда: https://dev.vk.com/reference/objects/photo-sizes#type
        # сортирую по типу потому что для фото загруженных до 2012 года значения height width равны '0'
        vk_size_type = 'sompqryzw'
        for img in res['items']:
            max_img = sorted(img['sizes'], key=lambda sz: vk_size_type.find(sz['type']), reverse=True)[0]
            images_info.append(
                {'size_type': max_img['type'], 'url': max_img['url'], 'likes_count': img['likes']['count']})
        return images_info

    def get_albums(self, user_id, count=0):
   #     params = {'access_token': self.token, 'owner_id': user_id, 'v': self.version}
        params = {**self.params}
        if count:
            params['count'] = count
        res = requests.get(self._get_api_url('photos.getAlbums'), params=params).json()
        return res