import requests
import json
from pprint import pprint
from tqdm import tqdm
from time import sleep

with open('text.txt', 'r') as f:
    token_vk = f.read().strip()

user_id = int(input('Ведите id пользователя: '))
token_ya = int(input('Ведите id пользователя: '))


def get_photos():
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': '1',
        'count': 10,
        'access_token': token_vk,
        'v': '5.131'
    }
    res = requests.get(url, params=params, timeout=5)
    return res.json()


def personal_info():
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'access_token': token_vk,
        'v': '5.131'
    }
    res = requests.get(url, params=params, timeout=5)
    info = res.json()['response'][0]['first_name'] + ' ' + res.json()['response'][0]['last_name']
    return info


def get_info():
    data_list = []
    photo_data = {}
    data = get_photos()
    x = -1
    for userpic in range(len(data['response']['items'])):
        if data['response']['items'][userpic]['likes']['count'] in photo_data:
            photo_data[data['response']['items'][userpic]['date']] = \
                data['response']['items'][userpic]['sizes'][-1]['url']
        else:
            photo_data[data['response']['items'][userpic]['likes']['count']] = \
                data['response']['items'][userpic]['sizes'][-1]['url']
    for name in photo_data:
        data_dict = {}
        x += 1
        data_dict['file_name'] = str(name)+'.jpeg'
        data_dict['size'] = data['response']['items'][x]['sizes'][-1]['type']
        data_list.append(data_dict)
    with open(f'{personal_info()}.json', 'w') as w_file:
        json.dump(data_list, w_file)
    return photo_data


def get_headers():
    return {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {token_ya}'
    }


def get_files_list():
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    headers = get_headers()
    response = requests.get(files_url, headers=headers, timeout=5)
    return response.json()


def new_folder():
    folder_name = personal_info()
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = get_headers()
    params = {'path': folder_name}
    requests.put(upload_url, headers=headers, params=params)
    return folder_name


def upload_photo_by_url():
    folder = new_folder()
    userpic_data = get_info()
    with tqdm(total=len(userpic_data), colour='green') as bar:
        for name in userpic_data:
            file_path = str(folder) + '/' + str(name) + '.jpeg'
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            url = userpic_data[name]
            headers = get_headers()
            params = {'path': file_path, 'url': url, 'overwrite': 'true'}
            requests.post(upload_url, headers=headers, params=params)
            sleep(0.1)
            bar.update(1)
        bar.close()
    with open(f'{personal_info()}.json', 'r') as r_file:
        pprint(json.load(r_file))


upload_photo_by_url()
