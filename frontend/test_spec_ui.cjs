const { Builder, By, until, logging } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');

async function runTest() {
  const prefs = new logging.Preferences();
  prefs.setLevel(logging.Type.BROWSER, logging.Level.ALL);

  let driver = await new Builder()
    .forBrowser('chrome')
    .setLoggingPrefs(prefs)
    .build();

  try {
    console.log("Navigating to frontend...");
    await driver.get('http://localhost:5174/new-analysis');
    
    console.log("Entering requirement...");
    const textarea = await driver.wait(until.elementLocated(By.tagName('textarea')), 10000);
    await textarea.sendKeys('We need to procure reinforcement steel bars for a new college building. The bars will be used in RCC columns, beams and slabs. We require 500 MPa grade deformed bars with suitable bendability, weldability, corrosion resistance, dimensional accuracy and quality certification. The supplier should provide test certificates and ensure that the material conforms to the applicable Indian Standard.');
    
    console.log("Clicking Analyze...");
    const analyzeBtn = await driver.findElement(By.xpath("//button[contains(text(), 'Analyze Requirement')]"));
    await analyzeBtn.click();
    
    console.log("Waiting for analysis results...");
    await driver.wait(until.elementLocated(By.xpath("//button[contains(text(), 'Find Applicable Standards')]")), 20000);
    
    console.log("Clicking Find Applicable Standards...");
    const findBtn = await driver.findElement(By.xpath("//button[contains(text(), 'Find Applicable Standards')]"));
    await findBtn.click();
    
    console.log("Waiting for recommendations...");
    await driver.wait(until.elementLocated(By.xpath("//button[contains(text(), 'Check Specification Gaps')]")), 30000);
    
    console.log("Clicking Check Specification Gaps...");
    const checkBtn = await driver.findElement(By.xpath("//button[contains(text(), 'Check Specification Gaps')]"));
    await checkBtn.click();

    console.log("Waiting a few seconds for potential white screen...");
    await driver.sleep(15000); // give it time to crash

    console.log("Fetching browser logs...");
    const logs = await driver.manage().logs().get(logging.Type.BROWSER);
    logs.forEach(entry => {
      console.log(`[${entry.level.name}] ${entry.message}`);
    });

  } catch(e) {
    console.error("Test failed:", e);
  } finally {
    await driver.quit();
  }
}

runTest();
