import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_browser_logs(driver):
    logs = driver.get_log('browser')
    for log in logs:
        print(f"BROWSER LOG: {log}")

def reproduce_bug():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    # Try different frontend ports
    ports = [5174]
    driver = None
    
    for port in ports:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(f"http://localhost:{port}/new-analysis")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
            )
            print(f"Connected to frontend on port {port}")
            break
        except Exception:
            if driver:
                driver.quit()
            driver = None

    if not driver:
        print("Could not connect to frontend")
        return False
        
    try:
        textarea = driver.find_element(By.CSS_SELECTOR, "textarea")
        textarea.send_keys("We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.")
        
        button = driver.find_element(By.XPATH, "//button[contains(., 'Analyze Requirement')]")
        button.click()
        
        print("Submitted requirement, waiting for extraction...")
        
        # Wait for "Find Applicable Standards" to appear
        find_btn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Find Applicable Standards')]"))
        )
        print("Requirement extracted. Clicking Find Applicable Standards...")
        
        get_browser_logs(driver)
        
        find_btn.click()
        
        print("Clicked Find Applicable Standards. Waiting for 3 seconds...")
        time.sleep(3)
        
        get_browser_logs(driver)
        
        print("Page source after clicking:")
        body = driver.find_element('tag name', 'body').text; print('BODY TEXT:\n', body[:2000])
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        get_browser_logs(driver)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    reproduce_bug()
