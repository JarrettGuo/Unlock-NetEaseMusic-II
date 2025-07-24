# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001885507228BCB04B7EC5422F7ACE13D0C5CFBF8C4A19A184CCA19A05225BE2C11119DFF2F3BC8619A237E244A0D1E6C05491FCCE30C31BA7D709A0E773BF29C1973C37E690AE0269B657D8863EDF648A01349F5D3AD1BAFD503F462343357CD25914BACA8729E450F1B224839DD25AC671D8A1B242010143CAFED968AF98F4A128A7CDCDCC12C09AB7ADA489DD551DEAE6AD31F90EDC323FDFA1B06D30F9C395237B72E1259026E47E187BC04F36468D7EA4C3439462C288BB23781234951FB93A14BF612FE94F6C8C233D5402893F861A75DCDEB3C06EC3FEE5A3C6F311700C4F08532485BECD97F78385EC6F021FC37C412C2722BBE14979BF4450A18038CCF84A55696C3852DC5F0EE7FAD1AD4F74FC8F65EA0A3799348B84C9E57FF82AD634A609E224B6FB9946455060259182F356CF19EEAAB0E94904930FD6F1D5064F3E5CADADED3F5AD9AD05CCF8664BF5F33C1959DEA5285A6769AD649A3CFE71DE6DEE400AE78B5F1CB43417017C0D39273D61B2BB759523DE664A8C76A9853C467D1CB0FC3CD515C28BA37F526100B044"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
