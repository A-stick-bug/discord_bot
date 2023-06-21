import os
import requests
import matplotlib.pyplot as plt

def get_current_weather(location):
    api_key = os.environ['WEATHER_API']
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes"

    response = requests.get(url)
    data = response.json()

    location = data['location']['name']
    country = data['location']['country']
    time = data['location']['localtime']
    last_updated = data["current"]['last_updated']
    temperature = data['current']['temp_c']
    condition = data['current']['condition']['text']
    wind_speed = data['current']['wind_kph']
    wind_dir = data['current']['wind_dir']
    pressure = data['current']['pressure_mb']
    precipitation = data['current']['precip_mm']
    feels_like = data['current']['feelslike_c']
    uv_index = data['current']['uv']
    visibility = data['current']['vis_km']
    humidity = data['current']['humidity']
    gust_speed = data['current']['gust_kph']

    aqi_data = data['current']['air_quality']
    aqi = aqi_data['us-epa-index']
    co = round(aqi_data['co'], 1)
    no2 = round(aqi_data['no2'], 1)
    o3 = round(aqi_data['o3'], 1)
    so2 = round(aqi_data['so2'], 1)
    pm2_5 = round(aqi_data['pm2_5'], 1)
    pm10 = round(aqi_data['pm10'], 1)

    res = f"## Weather in {location} ({country})\n"
    res += f"At **{time}**, it is **{condition.lower()}** with a " \
          f"temperature of **{temperature}°C**. It feels like **{feels_like}°C**. The wind is coming from " \
          f"the **{wind_dir}** direction at a speed of **{wind_speed} kph** with gusts up to **{gust_speed} " \
          f"kph**. The pressure is **{pressure} mb** and the precipitation is **{precipitation} mm**. The UV" \
          f" index is **{uv_index}**, the visibility is **{visibility} km**, and the humidity is **{humidity}%**.\n\n" 

    res += f'Air Quality Index (US EPA index): {aqi}\n'
    res += f'CO (Carbon Monoxide): {co}\n'
    res += f'NO2 (Nitrogen Dioxide): {no2}\n'
    res += f'O3 (Ozone): {o3}\n'
    res += f'SO2 (Sulfur Dioxide): {so2}\n'
    res += f'PM2.5 (Particulate Matter < 2.5 µm): {pm2_5}\n'
    res += f'PM10 (Particulate Matter < 10 µm): {pm10}\n\n'

    res += f"*(Weather data last updated at {last_updated})*\nData from https://www.weatherapi.com/"

    return res


    
def update_today_weather(location):
    api_key = os.environ['WEATHER_API']
    days = 1

    # fetch data
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}"
    response = requests.get(url)
    data = response.json()

    location = data['location']['name']
    country = data['location']['country']
    forecast_data = data["forecast"]["forecastday"]
    day = forecast_data[0]

    date = day["date"]
    hourly_data = day["hour"]
    max_temp = day["day"]["maxtemp_c"]
    min_temp = day["day"]["mintemp_c"]
    avg_temp = day["day"]["avgtemp_c"]
    max_wind = day["day"]["maxwind_kph"]
    total_precip = day["day"]["totalprecip_mm"]
    avg_humidity = day["day"]["avghumidity"]
    condition = day["day"]["condition"]["text"]
    uv_index = day["day"]["uv"]

    res = f"## Weather in {location} ({country}) - {date} \nHigh: **{max_temp}°C**, Low: **{min_temp}°C**, Avg: **{avg_temp}°C**\n"
    res += f"Max Wind: **{max_wind} kph**, Total Precipitation: **{total_precip} mm**, Avg Humidity: **{avg_humidity}%**\n"
    res += f"Condition: **{condition}**, UV Index: **{uv_index}**"
    
    # graphing temperature and precipitation
    hours = []
    temperatures = []
    precipitation = []

    for hour in hourly_data:
        time = hour["time"]
        temp_c = hour["temp_c"]
        precip_mm = hour["precip_mm"]

        # extract hour
        hour_str = time.split(" ")[1].split(":")[0] + ":00"
        hours.append(hour_str)
        temperatures.append(temp_c)
        precipitation.append(precip_mm)

    fig, ax1 = plt.subplots()

    # temperature
    ax1.plot(hours, temperatures, color="tab:red")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    # precipitation
    if total_precip > 0:
        ax2 = ax1.twinx()
        ax2.bar(hours, precipitation, color="tab:blue", alpha=0.45)
        ax2.set_ylabel("Precipitation (mm)", color="tab:blue")
        ax2.tick_params(axis="y", labelcolor="tab:blue")
    else:
        ax2 = ax1.twinx()
        ax2.bar(hours, precipitation, color="tab:blue", alpha=0.45)
        ax2.set_ylabel("(No Precipitation)", color="tab:blue")
        ax2.set_yticks([])


    # order to draw things
    ax1.set_axisbelow(True)
    ax1.grid(color="silver")
    ax1.set_zorder(2)
    ax2.set_zorder(1)
    ax1.patch.set_visible(False)

    # put label once every 4 ticks on x-axis
    tick_labels = [hour if i % 4 == 0 else "" for i, hour in enumerate(hours)]
    plt.xticks(hours, tick_labels)

    plt.title(f"{location} ({country}) - {date}")
    plt.savefig('today_temperature.png')
    plt.close()

    return res