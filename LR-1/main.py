import package 


if __name__ == '__main__':
    token = input('Введите токен от Яндекс.Диск')
    new_folder = input('Введите название папки')
    uploader = package.YaUploader(token)
    result = uploader.upload()
    downloader = package.YaDownloader(token)
    downloader.download()
