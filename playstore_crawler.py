import argparse

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


def write_text_file(file_path, data: list):
    with open(file_path, "w") as f:
        for d in data:
            f.write(f"{d}\n")


class PlayStoreCrawler:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
        options.add_argument('user-agent=' + user_agent)
        if self.headless:
            options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def scroll_and_collect(self, url, file_path=None):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        SCROLL_PAUSE_TIME = 2

        while True:
            for _ in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            try:
                self.driver.find_element(By.XPATH, "//span[@class='RveJvd snByac']")
            except:
                break

            if new_height == last_height:
                break
            last_height = new_height

        game_list = self.driver.find_elements(By.XPATH, "//div[@role='listitem']")
        game_id_list = [item.find_element(By.TAG_NAME, "a").get_attribute("href").split("?id=")[-1] for item in
                        tqdm(game_list) if "?id=" in item.find_element(By.TAG_NAME, "a").get_attribute("href")]

        if file_path:
            self._write_text_file(file_path, list(set(game_id_list)))
        return list(set(game_id_list))

    @staticmethod
    def _write_text_file(file_path, data: list):
        with open(f"{file_path}.txt", "w") as f:
            for d in data:
                f.write(f"{d}\n")

    def quit_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, default='https://play.google.com/store/games')
    parser.add_argument("--file_path", type=str, required=False,
                        help="Path to save the collected game IDs. If not provided, the method will return the values.")
    args = parser.parse_args()

    crawler = PlayStoreCrawler()

    if args.file_path:
        crawler.scroll_and_collect(args.url, args.file_path)
    else:
        collected_data = crawler.scroll_and_collect(args.url)
        print(f"Number of collected data: {len(collected_data)}")

    crawler.quit_driver()
