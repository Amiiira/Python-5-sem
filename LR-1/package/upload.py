import requests
from pprint import pprint

class YaUploader:
    def __init__(self, token: str):
        self.token = token 

    def create_disk(self):
        folder_name = input('Как хотите назвать вашу папку ? ')
        url = f'https://cloud-api.yandex.net/v1/disk/resources?path=%2F{folder_name}'
        headers = {
            "Authorization": self.token
        }
        try:
            response = requests.put(url, headers=headers)
            response.raise_for_status()
            return folder_name
        except Exception as e:
            print(f'Возникла ошибка при создании папки: {e}')
            return None

    def upload(self):
        destination = self.create_disk()
        print('Убедитесь, что файл располагается там же, где располагается фал main.py')
        file_name = input('Введите имя вашего файла: (не забудьте расширение: .jpg .txt и т.п.)')
        file_path = f'/{destination}/{file_name}'
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

        params = {
            "path": file_path
        }
        headers = {
            "Authorization": self.token
        }
        try:
            with open(file_name, 'rb') as file:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                url_for_upload = response.json().get('href', '')
                response2 = requests.put(url_for_upload, files={"file": file})
                response2.raise_for_status()
                print('!!!Файл успешно загружен!!!')
        except Exception as e:
            print(f'Возникла ошибка {e}')
