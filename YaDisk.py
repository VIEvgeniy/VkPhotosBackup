import requests

class YaDisk:
    def __init__(self, token):
        self.token = token
        self.host = 'https://cloud-api.yandex.net'
        self.file_api = '/v1/disk/resources/'

    def _get_api_url(self, api=''):
        res = f'{self.host}{self.file_api}{api}'
        return res

    def _get_headers(self):
        res = {'Authorization': f'OAuth {self.token}', 'Content-Type': 'application/json'}
        return res

    # get file list
    def list(self):
        res = requests.get(url=self._get_api_url('files'), headers=self._get_headers())
        return res.json()

    # upload file
    def uploads(self, path, filenames):
        params = {
            'overwrite': 'true'
        }
        for filename in filenames:
            params['path'] = f'{path}/{filename}'
            upload_url = requests.get(url=self._get_api_url('upload'), headers=self._get_headers(), params=params).json()
            res = requests.put(url=upload_url.get('href', ''), data=open(filename, 'rb'), params=params)
            res.raise_for_status()

    # create new directory
    def mkdir(self, path):
        params = {
            'path': path,
            'overwrite': 'true'
        }
        requests.put(url=self._get_api_url(), headers=self._get_headers(), params=params)
