# В URLFinder и будет срабатывать функция url_hook, которая и будет перехватывать ситуацию, в которой загрузка модуля 
# должна идти по URL-адресу

from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available
        
    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        
        else:
            return None

import re
import sys
from urllib.request import urlopen



def url_hook(some_str):
    try:
        import requests

        if not some_str.startswith(("http", "https")):
            raise ImportError
    
        response = requests.get(some_str)
        response.raise_for_status()
        data = response.text
        filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
        modnames = {name[:-3] for name in filenames}
        return URLFinder(some_str, modnames)
    except ImportError:
        print('URL не начинается с "http" или "https"')
    except requests.exceptions.RequestException as e:
        print('Возникла ошибка при подключении к серверу: {e}')


sys.path_hooks.append(url_hook)
print(sys.path_hooks)

# А теперь опишем функцию, в которой мы 
# для "перехваченного" адреса URL модуля будем делать импорт

from urllib.request import urlopen

class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)