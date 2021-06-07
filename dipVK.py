import requests
import json
import pprint
from pprint import pprint

class VKUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.version = version
        self.token = token
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url+'users.get', self.params).json()['response'][0]['id']

    def get_photo(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        url = 'https://api.vk.com/method/'
        photo_url = url + 'photos.get'
        photo_params = {
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1,
        }
        res = requests.get(photo_url, params={**self.params, **photo_params})
        vk_dict = res.json()
        vk_list = []
        vk_foto =[]
        vk_app = []
        for x in vk_dict['response']['items']:  # Как перебрать эти данные
            for y in x:
                print(y)



        return (vk_dict['response']['items'])


token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
vk_client = VKUser(token, '5.130')
pprint(vk_client.get_photo())

