import requests


class VkConnect:
    def __init__(self, token):
        self.token = token
        self.host = 'https://api.vk.com/method/'

    def _get_api_url(self, api=''):
        res = f'{self.host}{api}'
        return res
    def get_user_info(self, user_id, fields ):
        params = {
            access_token: self.token,
            user_id: user_id,
            fields: fields
        }
        res = requests.get(_get_api_url('user.get'), params = params)
        ret res.json()