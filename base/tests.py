import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

class TestWebApp:
    def setup_method(self):
        # Set the path to the chromedriver executable
        chrome_driver_path = "/usr/bin/google-chrome"
        self.driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))

    def teardown_method(self):
        self.driver.quit()

    def test_homepage(self):
        # Navigate to the web application
        self.driver.get("http://localhost:8000")

        # Wait for the page to load
        wait = WebDriverWait(self.driver, 500)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        print (self.driver.title)
        # Assert that the page title is correct
        assert "Otaku House - The #1 Anime Merchandise and Cosplay Sho." in self.driver.title

        # Assert that the "Welcome" message is present
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h1").text
        assert "LATEST PRODUCTS" in welcome_message