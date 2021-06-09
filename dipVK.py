import requests
import json
from pprint import pprint
from datetime import datetime
import time
from tqdm import tqdm
import os





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
        data_json_list = []

        for x in tqdm(vk_dict['response']['items']):
            file_url = x['sizes'][-1]['url']
            data_json = x['sizes'][-1]['type']
            file_name = str(x['likes']['count'])
            date = x['date']
            ts = int(date)
            ts_new = str(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))
            api = requests.get(file_url)
            file_name_new = file_name+"-likes-"+ts_new+".jpg"
            data_json_w = {}
            data_json_w["file_name"] = file_name_new
            data_json_w["size"] = data_json
            data_json_list.append(data_json_w)
            with open ("images/%s" % file_name_new, "wb") as f:
                f.write(api.content)

        with open('data.json', 'w', encoding='utf-8') as file:          #Запись в JSON файл
            json.dump(data_json_list, file)

        return print("Скачивание фото выполнено!")

    def upload(self, token_yandex):
    #на яндекс диске нужно создать папку images
        path = 'images/'
        files_list = os.listdir(path)
        data = os.path.join(path)
        #print(files_list)

        for z in tqdm(files_list):
            headers = {'Content-Type': 'application/json', 'Authorization': token_yandex}
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers_2 = headers
            params = {"path": data+z, "overwrite": "true"}
            response_2 = requests.get(upload_url, headers=headers_2, params=params)
            x = response_2.json()
            href = x.get("href")
            response_3 = requests.put(href, data=open(path+z, 'rb'))
            response_3.raise_for_status()

        return print("Фотографии загружены на диск!")





token_vk = '' #Токен ВК
token_yandex = '' #Токен яндекс диска
vk_client = VKUser(token_vk, '5.130')
vk_client.get_photo()
vk_client.upload(token_yandex)


