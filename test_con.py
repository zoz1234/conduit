from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from data_for_test import user, article
from func_for_test import sign_in, create_article
import time
import csv


class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    def test_open(self):
        main_logo = self.browser.find_element(By.LINK_TEXT, 'conduit')
        assert main_logo.text == "conduit"

    def test_accept(self):
        footer = self.browser.find_element(By.TAG_NAME, 'footer')
        accept_btn = footer.find_element(By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_btn.click()
        time.sleep(1)
        cookie_panel = self.browser.find_elements(By.ID, 'cookie-policy-panel')
        assert len(cookie_panel) == 0

    def test_sign_up(self):
        sing_up = self.browser.find_element(By.LINK_TEXT, 'Sign up')
        sing_up.click()

        username_input= WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Username"]')))
        email_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Password"]')))

        username_input.send_keys(user["name"])
        email_input.send_keys(user["email"])
        password_input.send_keys(user["password"])
        
        sing_up_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        sing_up_btn.click()

        message = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        assert message.text == "Welcome!"

        ok_btn = self.browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
        ok_btn.click()

        user_name = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[2]
        assert user_name.text == user["name"]
        
    def test_login(self):
        sign_in(self.browser)

        user_name = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[4]')))
        assert user_name.text == user["name"]
        
    def test_article_title_list(self):
        sign_in(self.browser)

        title_list = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="article-preview"]//a//h1')))
        assert len(title_list) != 0
    
    def test_pages(self):
        sign_in(self.browser)

        page_list = self.browser.find_elements(By.XPATH, '//a[@class="page-link"]')

        for page in page_list:
            page.click()
            active_page = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//li[@class="page-item active"]')))
            assert page.text == active_page.text
    
    def test_new_article(self):
        sign_in(self.browser)
        create_article(self.browser)

        author = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@class="author"]')))
        title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//h1')))

        assert author.text == user["name"]
        assert title.text == article["title"]
       
#     def test_edit_article(self):
#         sign_in(self.browser)
#         create_article(self.browser)

#         edit_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-edit"]')))
#         edit_btn.click()

#         title_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]')))
#         title_input.clear()
#         title_input.send_keys("Új cím")
#         time.sleep(2)

#         publish_btn = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
#         publish_btn.click()

#         title = WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]//h1')))

#         assert title.text == "Új cím"   

    def test_delete_article(self):
        sign_in(self.browser)
        create_article(self.browser)

        article_url = self.browser.current_url
        del_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-trash-a"]')))
        del_btn.click()
        #time.sleep(5)

        assert self.browser.current_url != article_url
        
    def test_save_data_to_file(self):
        sign_in(self.browser)
        time.sleep(1)

        # Az applikáció működése miatt, csak közvetlenül a felhasználó oldalára belépve
        # gyűjti ki csak a felhasználó által publicált cikkeket. 
        
        self.browser.switch_to.new_window()
        self.browser.get("http://localhost:1667/#/@testuser1")

        about_list = WebDriverWait(self.browser, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="article-preview"]//a//h1')))

        with open('abouts.csv', 'w') as file:
            writer = csv.writer(file)
            for about in about_list:
                writer.writerow([about.text])

        with open('abouts.csv', 'r') as file:
            first_row = file.readline().rstrip('\n')
            
            assert first_row == about_list[0].text
        
    def test_logout(self):
        sign_in(self.browser)

        logout = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log out')))
        logout.click()

        sign_in_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Sign in')))
        assert sign_in_btn.is_displayed()
        
