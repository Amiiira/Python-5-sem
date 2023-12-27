from xml.etree import ElementTree as ET
import requests
import time
import json
import csv

class BaseCurrenciesList:
    def __init__(self):
        self.tracked_currencies = []
        self.last_update_time = None

    def __del__(self):
        print("Объект удален.")

    def __repr__(self):
        return f"BaseCurrenciesList(tracked_currencies={self.tracked_currencies}, last_update_time={self.last_update_time})"

    def get_currencies(self):
        self.last_update_time = time.time()
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        xml_data = response.content

        root = ET.fromstring(xml_data)
        currencies_data = {}

        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = float(currency.find('Value').text.replace(',', '.'))
            currencies_data[code] = f"{value:.3f}"

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


# Декоратор JSON
class decorator_JSON:
    def __init__(self, component):
        self.component = component

    def jsonify(self):
        return json.dumps(self.component.get_currencies(), sort_keys=False, indent=2, ensure_ascii=False, separators=(',', ': '))


# Декоратор CSV
class decorator_CSV:
    def __init__(self, component):
        self.component = component

    def show_cur_save(self):
        cur_dict = self.component.get_currencies()
        currencies = []
        for code, value in cur_dict.items():
            cur = f"{float(value):.3f}" if '.' in value else value
            currencies.append({'code': code, 'value': value})
        header = ['code', 'value']
        with open('LR-7/save.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for row in currencies:
                writer.writerow(row)
        print('save.csv ready')


if __name__ == "__main__":
    base_component = BaseCurrenciesList()
    
    json_decorator = decorator_JSON(base_component)
    print(json_decorator.jsonify())
    
    csv_decorator = decorator_CSV(base_component)
    csv_decorator.show_cur_save()
