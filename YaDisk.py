import requests


class YaDisk:
    def __init__(self, token):
        self.token = token
        self.host = 'https://cloud-api.yandex.net/v1/disk/'
        self.file_api = 'resources/'

    def _get_api_url(self, api=''):
        res = f'{self.host}{self.file_api}{api}'
        return res

    def _get_headers(self):
        res = {'Authorization': f'OAuth {self.token}', 'Content-Type': 'application/json'}
        return res

    # get file list
    def list(self):
        res = requests.get(url=self._get_api_url('files'), headers=self._get_headers())
        if res.ok:
            return res.json()

    def info(self):
        res = requests.get(url=self.host, headers=self._get_headers())
        if res.ok:
            return res.json()

    # upload files
    def uploads(self, path, filenames):
        params = {
            'overwrite': 'true'
        }
        for filename in filenames:
            params['path'] = f'{path}/{filename}'
            upload_url = requests.get(url=self._get_api_url('upload'), headers=self._get_headers(),
                                      params=params).json()
            res = requests.put(url=upload_url.get('href', ''), data=open(filename, 'rb'), params=params)
            res.raise_for_status()

    # загрузить данные из data на яндекс диск, fullpath - полный путь до файла на яндекс диске
    def upload(self, fullpath, data):
        params = {'overwrite': 'true', 'path': fullpath}
        upload_url = requests.get(url=self._get_api_url('upload'), headers=self._get_headers(), params=params).json()
        res = requests.put(url=upload_url.get('href', ''), data=data, params=params)
        res.raise_for_status()

    # загрузить данные из интернета на яндекс диск, fullpath - полный путь до файла на яндекс диске
    def upload_from_url(self, fullpath, url):
        params = {'path': fullpath, 'url': url}
        res = requests.post(headers=self._get_headers(), url=self._get_api_url('upload'), params=params)
        res.raise_for_status()
    # create new directory
    def mkdir(self, path):
        params = {
            'path': path,
            'overwrite': 'true'
        }
        res = requests.put(url=self._get_api_url(), headers=self._get_headers(), params=params)
        return res.ok
