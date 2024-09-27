# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import os
import whisper
import warnings

warnings.filterwarnings("ignore")

model = whisper.load_model("base")


def transcribe(url):
    with open(".temp", "wb") as f:
        f.write(requests.get(url).content)
    result = model.transcribe(".temp")
    return result["text"].strip()


def click_checkbox(driver):
    driver.switch_to.default_content()
    time.sleep(0.5)
    driver.switch_to.frame(
        driver.find_element(By.XPATH, ".//iframe[contains(@title, 'reCAPTCHA')]")
    )
    time.sleep(0.5)
    driver.find_element(By.ID, "recaptcha-anchor").click()
    time.sleep(0.5)
    driver.switch_to.default_content()
    time.sleep(0.5)


def request_audio_version(driver):
    driver.switch_to.default_content()
    time.sleep(0.5)
    driver.switch_to.frame(
        driver.find_element(
            By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"
        )
    )
    time.sleep(0.5)
    driver.find_element(By.ID, "recaptcha-audio-button").click()
    time.sleep(0.5)


def solve_audio_captcha(driver):
    text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute("src"))
    time.sleep(0.5)
    driver.find_element(By.ID, "audio-response").send_keys(text)
    time.sleep(0.5)
    driver.find_element(By.ID, "recaptcha-verify-button").click()
    time.sleep(0.4)


if __name__ == "__main__":
    driver = webdriver.Chrome()

    driver.get("https://app.nodepay.ai/login")
    click_checkbox(driver)
    time.sleep(1)
    request_audio_version(driver)
    time.sleep(1)
    solve_audio_captcha(driver)
    time.sleep(10)
