import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def run_test():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:5174/new-analysis")
    time.sleep(3)
    
    req_input = driver.find_element(By.ID, "requirement")
    req_input.send_keys("We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.")
    
    analyze_btn = driver.find_element(By.XPATH, "//button[contains(., 'Analyze Requirement')]")
    analyze_btn.click()
    print("Clicked Analyze")
    time.sleep(12)
    
    try:
        find_btn = driver.find_element(By.XPATH, "//button[contains(., 'Find Applicable Standards')]")
        find_btn.click()
        print("Clicked Find Applicable Standards")
    except Exception as e:
        print("Could not find button:", e)
        
    time.sleep(5)
    
    print("Browser Logs:")
    for log in driver.get_log('browser'):
        print(log)
        
    driver.quit()

if __name__ == "__main__":
    run_test()
