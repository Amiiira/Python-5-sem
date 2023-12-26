import requests
import xml.etree.ElementTree as ET
import time

class CurrencyTracker:
    def __init__(self):
        self.tracked_currencies = []
        self.last_update_time = None

    def __del__(self):
        print("Объект удален.")

    def __repr__(self):
        return f"CurrencyTracker(tracked_currencies={self.tracked_currencies}, last_update_time={self.last_update_time})"

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

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        currencies_data = self.get_currencies()

        tracked_currencies_data = {
            currency: float(currencies_data.get(currency, 0).replace(',', '.')) for currency in self.tracked_currencies
        }

        plt.figure(figsize=(10, 6))
        bars = plt.bar(tracked_currencies_data.keys(), tracked_currencies_data.values(), width= 0.5, color='m', alpha=0.4)
        plt.title('График курс валют')
        plt.xlabel('Код валюты')
        plt.ylabel('Курс валюты')
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, max(tracked_currencies_data.values()) + 10)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{round(yval, 2)} ₽', ha='center', va='bottom', weight='bold')

        plt.tight_layout()
        plt.savefig('LR-5/currencies.jpg')
        plt.show()


# Пример использования класса
if __name__ == "__main__":
    tracker = CurrencyTracker()

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

    tracker.visualize_currencies()

    # Вызов деконструктора
    del tracker
