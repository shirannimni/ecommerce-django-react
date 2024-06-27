import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class TestWebApp:
    def setup_method(self):
        # Set the path to the chromedriver executable
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignor-certificate-errors")
        chrome_options.add_argument("--test-type")

        chrome_options.binary_location = "/opt/google/chrome/chrome"


         try:
        
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver path: {driver_path}")

        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
      except Exception as e:
        print(f"Error initializing WebDriver: {str(e)}")
        raise




        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="126.0.6478.126").install()), options=chrome_options)
        
        #driver_path = ChromeDriverManager().install()
        #self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        

         



    def teardown_method(self):
        self.driver.quit()

    def test_homepage(self):
        # Navigate to the web application
        self.driver.get("http://localhost:8000")

        # Wait for the page to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

        # Assert that the page title is correct
        assert "ecommerce-django-react" in self.driver.title

        # Assert that the "Welcome" message is present
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h1").text
        assert "Welcome" in welcome_message
