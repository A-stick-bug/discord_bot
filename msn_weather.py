from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image


def update_msn_weather(location):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1000,700)

    # Navigate to the webpage
    driver.get(f'https://www.msn.com/en-ca/weather/forecast/in-{location}')
    loc = driver.execute_script("return document.querySelector('#WeatherOverviewLocationName a').textContent")

    driver.save_screenshot("msn_weather.png")
    driver.quit()
    
    image = Image.open("msn_weather.png")
    crop_box = (30, 230, 636, 494)
    cropped_image = image.crop(crop_box)
    cropped_image.save("msn_weather.png")
    return loc


def update_weather_graph(location):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1500,1000)

    # Navigate to the webpage
    driver.get(f'https://www.msn.com/en-ca/weather/forecast/in-{location}')
    loc = driver.execute_script("return document.querySelector('#WeatherOverviewLocationName a').textContent")
      
    driver.execute_script("document.body.style.zoom='150%'")
    driver.execute_script("window.scrollBy(0, 2000)")
    time.sleep(6)
    driver.save_screenshot("msn_weather_graph.png")
    driver.quit()
    
    image = Image.open("msn_weather_graph.png")
    crop_box = (11, 369, 1375, 784)
    cropped_image = image.crop(crop_box)
    cropped_image.save('msn_weather_graph.png')
    
    return loc


if __name__ == '__main__':
    loc = "new york"
    print(update_msn_weather(loc))
