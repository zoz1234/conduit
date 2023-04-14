from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from data import user

def sign_in(browser):
    sign_in_btn = browser.find_element(By.LINK_TEXT, 'Sign in')
    sign_in_btn.click()

    email_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]')))
    email_input.send_keys(user["email"])

    password_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Password"]')))
    password_input.send_keys(user["password"])

    sign_in_btn2 = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
    sign_in_btn2.click()
