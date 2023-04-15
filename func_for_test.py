from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from data_for_test import user, article

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

def create_article(browser):
    new_art_btn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'New Article')))
    new_art_btn.click()

    title_input = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]')))
    about_input = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control"]')))
    article_text_input = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')))
    tags_input = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter tags"]')))

    title_input.send_keys(article["title"])
    about_input.send_keys(article["about"])
    article_text_input.send_keys(article["content"])
    tags_input.send_keys(article["tags"])

    publish_btn = browser.find_element(By.XPATH, '//button[@type="submit"]')
    publish_btn.click()

