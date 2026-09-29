from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def run_test():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)
    try:
        print("Navigating to http://localhost:5174/new-analysis")
        driver.get("http://localhost:5174/new-analysis")
        
        # Wait for textarea
        print("Waiting for textarea...")
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "requirement"))
        )
        print("Entering requirement text...")
        textarea.send_keys("We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.")
        
        # Click Analyze
        print("Clicking Analyze Requirement...")
        analyze_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze Requirement')]")
        analyze_btn.click()
        
        # Wait for "Find Applicable Standards" button
        print("Waiting for 'Find Applicable Standards' button...")
        find_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Find Applicable Standards')]"))
        )
        
        # Click Find Standards
        print("Clicking Find Applicable Standards...")
        # Since it might have an icon, search for text
        find_btn.click()
        
        # Wait for recommendations
        print("Waiting for recommendations to load...")
        rec_header = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Recommended Indian Standards')]"))
        )
        time.sleep(2)  # Let it render
        
        # Click "View Recommendation Evidence" on first one
        print("Clicking View Recommendation Evidence...")
        evidence_btn = driver.find_elements(By.XPATH, "//button[contains(., 'View Recommendation Evidence')]")
        if evidence_btn:
            driver.execute_script("arguments[0].scrollIntoView(true);", evidence_btn[0])
            evidence_btn[0].click()
            time.sleep(1)
        
        driver.save_screenshot("C:/Users/iamfa/.gemini/antigravity-ide/brain/576973ec-b367-4d87-8ee5-cbdabab6fb8d/frontend_test.png")
        print("Screenshot saved to frontend_test.png in artifacts directory")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
