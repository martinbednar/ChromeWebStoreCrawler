# Author: Martin Bednar (2024)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re




driver = webdriver.Chrome()




##### Get webpage with all Privacy and Security extensions on Chrome Web Store #####
driver.get("https://chromewebstore.google.com/category/extensions/make_chrome_yours/privacy")




##### Expand the list of all extensions on Chrome Web Store webpage #####
i=1
while (True):
    try:
        # Click on the "Load more" button if exists
        loadmore_button = driver.find_element(By.CLASS_NAME, "mUIrbf-LgbsSe")
    except:
        # Stop if "Load more" button does not exists - all extensions were loaded
        # print(i) # i*32 = aproximate total number of loaded extensions
        break
    loadmore_button.click();
    i+=1
    time.sleep(1)
    # Scroll bottom to the footer - just for visual checking of newly loaded extensions
    footer = driver.find_element(By.ID, "ZCHFDb")
    footer.location_once_scrolled_into_view




##### Get all extensions ids #####
extensions = driver.find_elements(By.XPATH, '//*[@data-item-id]')
extensions_ids = [extension.get_attribute('data-item-id').strip() for extension in extensions]




##### For each extension: Write all information about extension to the CSV file. #####
with open("PrivacyAndSecurityExtensions.csv", "w", encoding="utf-8") as f:
    f.write("Name;Id;E-mail;Number of users;Rating;Number of ratings;Repository\n")
    
    for extension_id in extensions_ids:
        name = ""
        email = ""
        numberofusers = ""
        rating = ""
        numberofratings = ""
        
        try:
            # Get a webpage of the the extension on Chrome Web Store
            driver.get("https://chromewebstore.google.com/detail/" + extension_id)
        except:
            print("Unable to load a webpage for the extension with id: " + extension_id)
            continue
        
        try:    
            name_elem = driver.find_element(By.CLASS_NAME, "Pa2dE")
            name = name_elem.text.strip()
        except:
            pass

        try:
            arrow = driver.find_element(By.CLASS_NAME, "gotS2b")
            arrow.click()
            email_elem = driver.find_element(By.CLASS_NAME, "AxYQf")
            email = email_elem.text.strip()
        except:
            pass

        try:
            numberofusers_elem = driver.find_element(By.CLASS_NAME, "F9iKBc")
            numberofusers = numberofusers_elem.text.replace('Extension', '').replace('Privacy & Security', '').replace('users', '').replace('user', '').replace(',', '').strip()
        except:
            pass

        try:
            rating_elem = driver.find_element(By.CLASS_NAME, "Vq0ZA")
            rating = rating_elem.text.replace('.', ',').strip()
        except:
            pass

        try:
            numberofratings_elem = driver.find_element(By.CLASS_NAME, "xJEoWe")
            numberofratings = numberofratings_elem.text.replace('ratings', '').replace('rating', '').strip()
            if '.' in numberofratings:
                numberofratings = numberofratings.replace('K', '00').replace('.', '').strip()
            else:
                numberofratings = numberofratings.replace('K', '000').replace('.', '').strip()
        except:
            pass
        
        try:
            overview = driver.find_element(By.CLASS_NAME, "JJ3H1e")
            # Regular expresions inspired by https://stackoverflow.com/a/59008843
            githublab_regex=re.compile('(?:https?://)?(?:www[.])?git(?:hub|lab)[.](?:com|org)/[\w-]+/[\w-]+\s?')
            git_links = set(link.strip() for link in githublab_regex.findall(overview.text))
            bitbucket_regex = re.compile('(?:https?://)?(?:www[.])?bitbucket[.](?:com|org)/[\w\-/]+\s?')
            git_links.update(set(link.strip() for link in bitbucket_regex.findall(overview.text)))
            git_links = ','.join(git_links)
        except:
            pass
    
        f.write(name + ";" + extension_id + ";" + email + ";" + numberofusers + ";" + rating + ";" + numberofratings + ";" + git_links + "\n")



driver.quit()
