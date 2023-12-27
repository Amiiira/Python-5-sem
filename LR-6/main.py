import requests
import xml.etree.ElementTree as ET
import time

def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()  
        return instances[cls]

    return getinstance

@singleton
class CurrencyTracker:
    def __init__(self):
        self.tracked_currencies = []
        self.last_update_time = None

    def __del__(self):
        print("Объект удален.")

    def __repr__(self):
        return f"CurrencyTracker(tracked_currencies={self.tracked_currencies}, last_update_time={self.last_update_time})"

    def get_currencies(self):
        current_time = time.time()
        if self.last_update_time is not None and current_time - self.last_update_time < 1:
            return self.cached_currencies

        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        if response.status_code != 200:
            print(f"Ошибка при запросе данных. Код ошибки: {response.status_code}")
            return None  

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            print(f"Ошибка при парсинге XML: {e}")
            return None  

        currencies_data = {}
        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = float(currency.find('Value').text.replace(',', '.'))
            currencies_data[code] = f"{value:.3f}"

        self.last_update_time = current_time
        self.cached_currencies = currencies_data
        return currencies_data

    def get_currency_value(self, currency_code):
        currencies_data = self.get_currencies()
        return currencies_data.get(currency_code)

    def add_tracked_currency(self, currency_code):
        if currency_code not in self.tracked_currencies:
            self.tracked_currencies.append(currency_code)
            print(f"Код {currency_code} добавлен в отслеживаемые валюты.")

    def get_tracked_currencies(self):
        return self.tracked_currencies

    def set_tracked_currencies(self, currencies):
        self.tracked_currencies = currencies




# Пример использования класса
if __name__ == "__main__":
    tracker = CurrencyTracker()
    tracker1 = CurrencyTracker()
    tracker2 = CurrencyTracker()

    print(tracker1 is tracker2)

    # Получение и вывод всех валют
    all_currencies = tracker.get_currencies()
    print("Все валюты:", all_currencies)

    # Получим курс дирхама ОАЭ
    aed_value = tracker.get_currency_value('AED')
    print("AED стоит:", aed_value, "₽")

    # Получим курс Катарского риала
    qar_value = tracker.get_currency_value('QAR')
    print("QAR стоит:", qar_value, "₽")

    # Добавление новой валюты в список отслеживаемых
    tracker.add_tracked_currency('IDR')

    # Список отслеживаемых валют
    tracked_currencies = tracker.get_tracked_currencies()
    print("Отслеживаемые валюты:", tracked_currencies)

    # Изменение списка отслеживаемых валют
    tracker.set_tracked_currencies(['AED', 'QAR', 'EGP'])

    # Вызов деконструктора
    del tracker
