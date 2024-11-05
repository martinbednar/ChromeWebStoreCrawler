from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
# Get webpage with Privacy and Security extension on Chrome Web Store
driver.get("https://chromewebstore.google.com/category/extensions/make_chrome_yours/privacy")

i=1
while (True):
    try:
        # Click on the "Load more" button if exists
        button = driver.find_element(By.CLASS_NAME, "mUIrbf-LgbsSe")
    except:
        # Stop if "Load more" button does not exists - all extensions were loaded
        print(i) # i*32 = aproximate total number of loaded extensions
        break
    button.click();
    i+=1
    time.sleep(1)
    # scroll bottom to footer - just for checking
    footer = driver.find_element(By.ID, "ZCHFDb")
    footer.location_once_scrolled_into_view

# Get all extensions ids
extensions = driver.find_elements(By.XPATH, '//*[@data-item-id]')

# Write all extensions ids to the file.
with open("PrivacyAndSecurityExtensionsIds.txt", "a") as f:
    for extension in extensions:
        f.write(extension.get_attribute('data-item-id') + "\n")
