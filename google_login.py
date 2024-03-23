import os
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from google_api import YoutubeAgent

SCROLL_PAUSE_TIME = 3


def init_driver():
    username = os.getlogin()

    options = Options()
    options.add_argument(f"user-data-dir=c:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\")

    return webdriver.Chrome(options=options)


def scrape_watch_later_playlist(driver):
    driver.get("https://www.youtube.com/playlist?list=WL")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
        time.sleep(SCROLL_PAUSE_TIME)
        height = driver.execute_script("return document.documentElement.scrollHeight")
        if height == last_height:
            break
        last_height = height

    videos = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="video-title"]'))
    )

    def parse_video_id(video):
        import urllib.parse

        url = video.get_attribute('href')
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        return video_id

    ids = list(map(lambda x: parse_video_id(x), videos))
    return ids


def main():
    # TODO add auto-closing in app authorization
    youtube = YoutubeAgent()
    driver = init_driver()
    video_ids = scrape_watch_later_playlist(driver)
    response = youtube.get_videos_details(video_ids)
    print(response)


if __name__ == '__main__':
    main()
