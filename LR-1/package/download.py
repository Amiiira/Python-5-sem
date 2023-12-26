import os
import requests

class YaDownloader:
    def __init__(self, token: str):
        self.token = token

    def download(self,):
        filename = input('Укажите название файла с расширением: ')
        file_path_on_disk = f'/{filename}'
        url = f'https://cloud-api.yandex.net/v1/disk/resources/download?path={file_path_on_disk}'
        headers = {
            "Authorization": f"OAuth {self.token}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            download_url = response.json().get('href', '')
            
            if download_url:
                response = requests.get(download_url)
                response.raise_for_status()
                
                current_directory = os.getcwd()
                local_file_path = os.path.join(current_directory, os.path.basename(file_path_on_disk))
                
                with open(local_file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Файл успешно скачан в {local_file_path}')
            else:
                print('Не удалось получить URL для скачивания файла.')
        except Exception as e:
            print(f'Возникла ошибка : {e}')




