from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
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
        cookie_panel = self.browser.find_elements(By.ID, 'cookie-policy-panel')
        assert len(cookie_panel) == 0
