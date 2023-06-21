import os
import requests
from datetime import datetime, timedelta


async def fetch_pic(date):
    api_key = os.environ['NASA_API']
    
    if date:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
    else:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    # fetching data
    response = requests.get(url)
    data = response.json()
    
    date = data["date"]
    title = data["title"]
    image_url = data["url"]
    hd_url = data["hdurl"] if "hdurl" in data.keys() else data["url"]
    description = data["explanation"]
    
    if hd_url == image_url:
        result = f"Date: {date}\n\n{title}\nURL to image: {image_url}\n\n{description}"
    else:
        result = f"Date: {date}\n\n{title}\nURL to image: <{image_url}>\nHigh Resolution Image: {hd_url}\n\n{description}"
        
    return (result,date)


def date_changer(date: str, command: str):
    current = datetime.strptime(date, '%Y-%m-%d')

    if command == '<':
        current -= timedelta(days=1)
        return current.strftime('%Y-%m-%d')
    else:
        current += timedelta(days=1)
        return current.strftime('%Y-%m-%d')

