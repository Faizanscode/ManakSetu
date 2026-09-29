import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify_phase5():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Try different frontend ports
    ports = [5176]
    driver = None
    
    for port in ports:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(f"http://localhost:{port}/analyze")
            # Wait to see if page loads
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
        textarea.send_keys("We need fire resistant steel doors for our new factory.")
        
        button = driver.find_element(By.XPATH, "//button[contains(., 'Analyze Requirement')]")
        button.click()
        
        print("Submitted requirement, waiting for results...")
        
        # Wait up to 30 seconds for recommendations to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'Why recommended:')]"))
        )
        print("Results loaded.")
        
        # Click on "View Evidence & Details"
        details_button = driver.find_element(By.XPATH, "//button[contains(., 'View Evidence & Details')]")
        details_button.click()
        time.sleep(1)
        
        # Verify new Evidence UI components are present
        page_source = driver.page_source
        
        assert "Why This Standard" in page_source, "Missing 'Why This Standard' section"
        assert "Score Breakdown" in page_source, "Missing 'Score Breakdown' section"
        assert "Standard Information" in page_source, "Missing 'Standard Information' section"
        assert "Sources" in page_source, "Missing 'Sources' section"
        assert "Source information is provided from the ManakSetu knowledge base" in page_source, "Missing disclaimer"
        
        print("SUCCESS: Phase 5 UI is correctly rendering the new Evidence, Explanation, Score Breakdown, and Sources structure.")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    verify_phase5()
