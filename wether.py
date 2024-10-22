import requests#библиотека для отправления запросов на сайт
import time

rus = {
''
}

par = {
"lang":"ru",
"lat": 50.4123,
"lon": 30.36019,
"appid": "84061a2a5ff54b490d63bd38d557b06d",
"units": "metric"
}

def get_wether():

    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params = par)
    r_hourly = requests.get('http://api.openweathermap.org/data/2.5/forecast', params = par)
    data = r.json()
    print('**', end ='')
    descript = data.get("weather")[0].get("description")
    print(descript, end = '')
    print('**')
    temp = data.get("main").get("temp")
    #temp = round(1.8(temp-273)+32)
    #temp = round((5/9)(temp-32))
    print("Температура(C)",temp)
    hum = data.get("main").get("humidity")
    print(f"Влажность {hum}%")
    wind_speed = data.get("wind").get("speed")
    print('Скорость ветра', wind_speed)
    wether = f"Температура(C) {temp},Влажность {hum} %,Скорость ветра {wind_speed} "
    return wether