import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

class TestWebApp:
    def setup_method(self):
        # Set the path to the chromedriver executable
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--ignor-certificate-errors")
        #chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")

        #chrome_options.binary_location = "/opt/google/chrome/chrome"

        
        #capabilities = DesiredCapabilities.CHROME.copy()
        #capabilities['pageLoadStrategy'] = 'normal'
        
        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
        #                               options=chrome_options,
        #                               desired_capabilities=capabilities)
        #self.driver.set_page_load_timeout(20)
         
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        request.cls.driver = driver
        yield
        driver.quit()
        

       # try:
        #    driver_path = ChromeDriverManager().install()
         #   print(f"ChromeDriver path: {driver_path}")
          #  self.driver = webdriver.Chrome(service=Service(driver_path), 
         #                                  options=chrome_options,
         #                                  desired_capabilities=capabilities)
         #   self.driver.set_page_load_timeout(30) 
        #except Exception as e:
         #  print(f"Error initializing WebDriver: {str(e)}")
          # raise




        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="126.0.6478.126").install()), options=chrome_options)
        
        #driver_path = ChromeDriverManager().install()
        #self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        

         



    def teardown_method(self):
        #self.driver.quit()
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_homepage(self):
        try:
            docker_host_ip = os.environ.get('DOCKER_HOST_IP', 'localhost')
            self.driver.get(f"http://{docker_host_ip}:5000")

            # Wait for the page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

            # Assert that the page title is correct
            assert "ecommerce-django-react" in self.driver.title

            # Assert that the "Welcome" message is present
            welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h1").text
            assert "Welcome" in welcome_message
        except Exception as e:
            print(f"Error during test: {str(e)}")
            raise

        #docker_host_ip = os.environ.get('DOCKER_HOST_IP', 'localhost')
        #self.driver.get(f"http://{docker_host_ip}:5000") 

        
        #self.driver.get("http://localhost:5000")

        # Wait for the page to load
        #wait = WebDriverWait(self.driver, 10)
        #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

        # Assert that the page title is correct
        #assert "ecommerce-django-react" in self.driver.title

        # Assert that the "Welcome" message is present
        #welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h1").text
        #assert "Welcome" in welcome_message
