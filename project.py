import requests
from pprint import pprint
from tqdm import tqdm
from time import sleep

with open('text.txt', 'r') as f:
    token_vk = f.read().strip()

with open('text2.txt', 'r') as file:
    token_ya = file.read().strip()

user_id = 20846303
# token ввод


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
    photo_data = {}
    data = get_photos()
    for userpic in range(len(data['response']['items'])):
        if data['response']['items'][userpic]['likes']['count'] in photo_data:
            photo_data[data['response']['items'][userpic]['date']] = \
                data['response']['items'][userpic]['sizes'][-1]['url']
        else:
            photo_data[data['response']['items'][userpic]['likes']['count']] = \
                data['response']['items'][userpic]['sizes'][-1]['url']
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
    with tqdm(total=100, colour='green') as bar:
        for name in userpic_data:
            file_path = str(folder) + '/' + str(name) + '.jpeg'
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            url = userpic_data[name]
            headers = get_headers()
            params = {'path': file_path, 'url': url, 'overwrite': 'true'}
            requests.post(upload_url, headers=headers, params=params)
            sleep(0.1)
            bar.update(10)
        bar.close()


upload_photo_by_url()