import os
from pprint import pprint

api_key = os.environ['...']

def get_weather_data(city, key):
  import requests
  import json
  
  if type(city) is not str:
    raise ValueError('параметр city не является строкой')
  if not api_key:
    raise ValueError('ключ для отправки запросов к API не задан')

  query = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
  try:
    r = requests.get(query)

        
  except requests.RequestException as e:
    print(f'Ошибка отправки или получения ответа от API openweathermap.org: {e}')
  else:
    if r.status_code == 200:
      data = r.json()
      city = data['name']
      code_country = data['sys']['country']
      lat = data['coord']['lat']
      lon = data['coord']['lon']
      zone = int(data['timezone'] / 60 / 60)
      if zone > 0:
        zone = '+' + str(zone)
      else:
        zone = str(zone)
      temperature = int(data['main']['feels_like'])
      info = {
        'City': city,
        'Country code': code_country,
        'Coordinates': {
        'Latitude': lat,
        'Longitude': lon,},
        'Timezone': f'UTC{zone}',
        'Temperature': temperature
      }
      
      '''  информацию о названии города (в контексте openweathermap),
           код страны (2 символа),
           широту и долготу, на которой он находится,
           его временной зоне,
           а также о значении температуры (как она ощущается).'''
      return json.dumps(info)
  if r.status_code == 404:
    print('В параметрах запроса ошибка. Ответ 404')


if __name__ == '__main__':
  pprint(get_weather_data('New York', key=api_key))
  pprint(get_weather_data('Chicago', key=api_key))
  pprint(get_weather_data('Saint Petersburg', key=api_key))
  pprint(get_weather_data('Dhaka', key=api_key))
