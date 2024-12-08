# Author: Martin Bednar (2024)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from git import Repo
from datetime import datetime
import os
from pathlib import Path




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
    f.write("Name;Id;E-mail;E-mails from repos;Number of users;Rating;Number of ratings;Repository\n")
    
    for extension_id in extensions_ids:
        name = ""
        email = ""
        numberofusers = ""
        rating = ""
        numberofratings = ""
        
        # Load a webpage of the the extension on Chrome Web Store
        try:
            # Get a webpage of the the extension on Chrome Web Store
            driver.get("https://chromewebstore.google.com/detail/" + extension_id)
        except:
            print("Unable to load a webpage for the extension with id: " + extension_id)
            continue
        
        # Get name of the extension
        try:    
            name_elem = driver.find_element(By.CLASS_NAME, "Pa2dE")
            name = name_elem.text.strip()
        except:
            pass

        # Get e-mail contact of the extension
        try:
            arrow = driver.find_element(By.CLASS_NAME, "gotS2b")
            arrow.click()
            email_elem = driver.find_element(By.CLASS_NAME, "AxYQf")
            email = email_elem.text.strip()
        except:
            pass

        # Get number of users of the extension
        try:
            numberofusers_elem = driver.find_element(By.CLASS_NAME, "F9iKBc")
            numberofusers = numberofusers_elem.text.replace('Extension', '').replace('Privacy & Security', '').replace('users', '').replace('user', '').replace(',', '').strip()
        except:
            pass

        # Get rating of the extension
        try:
            rating_elem = driver.find_element(By.CLASS_NAME, "Vq0ZA")
            rating = rating_elem.text.replace('.', ',').strip()
        except:
            pass

        # Get number of ratings of the extension
        try:
            numberofratings_elem = driver.find_element(By.CLASS_NAME, "xJEoWe")
            numberofratings = numberofratings_elem.text.replace('ratings', '').replace('rating', '').strip()
            if '.' in numberofratings:
                numberofratings = numberofratings.replace('K', '00').replace('.', '').strip()
            else:
                numberofratings = numberofratings.replace('K', '000').replace('.', '').strip()
        except:
            pass
        
        # Get links to the repositories of the extension
        try:
            overview = driver.find_element(By.CLASS_NAME, "JJ3H1e")
            # Regular expresions inspired by https://stackoverflow.com/a/59008843
            githublab_regex=re.compile('(?:https?://)?(?:www[.])?git(?:hub|lab)[.](?:com|org)/[\w-]+/[\w-]+\s?')
            git_links = set(link.strip() for link in githublab_regex.findall(overview.text))
            bitbucket_regex = re.compile('(?:https?://)?(?:www[.])?bitbucket[.](?:com|org)/[\w\-/]+\s?')
            git_links.update(set(link.strip() for link in bitbucket_regex.findall(overview.text)))
        except:
            pass
        
        # Clone repositories of the extension to the local directory "./repos"
        REPOS_DIRECTORY = "./repos"

        if not os.path.exists(REPOS_DIRECTORY):
            os.makedirs(REPOS_DIRECTORY)

        already_downloaded_repos = [name.split(' ')[0]+"_"+name.split(' ')[2] for name in os.listdir(REPOS_DIRECTORY)]
        
        for repo_url in git_links:
            if "bitbucket" in repo_url:
                print("Bitbucket repository: " + repo_url)
                print("Repository not cloned: " + extension_id+"_"+repo_url.split('/')[-1] + " (" + repo_url + ")")
                print("Bitbucket repositories are not cloned because they require authentication and the credentials are not provided in this script")
                continue
            if extension_id+"_"+repo_url.split('/')[-1] in already_downloaded_repos:
                print("Repository already downloaded: " + extension_id+"_"+repo_url.split('/')[-1] + " (" + repo_url + ")")
                continue
            try:
                repo = Repo.clone_from(repo_url, REPOS_DIRECTORY + "/" + extension_id + " - " + repo_url.split('/')[-1] + " - " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            except:
                print("Error cloning repository: " + repo_url)
                continue
        
        # Find e-mails in the cloned repositories of the extension
        email_regex = re.compile(r"[a-zA-Z0-9_.+#~-]+@[a-zA-Z0-9-]*[a-zA-Z]+[a-zA-Z0-9-]*\.[a-zA-Z0-9-.]+[a-zA-Z0-9]+")
        # Exclude e.g. arrow@2x.png (It looks like an e-mail address but it is not. It is a file according to filename extension ".png".)
        filetypes_regex = re.compile(r".*\.(png|jpg|jpeg|gif|bmp|tiff|tif|svg|ico|pdf|doc|docx|xls|xlsx|ppt|pptx|txt|csv|js|json|xml|zip|rar|tar|gz|7z|exe|msi|apk|dmg|iso|bin|jar|war|ear|mp3|mp4|avi|mkv|mov|flv|wmv|wma|wav|ogg|mpg|mpeg|flac|aac|aiff|amr|ape|asf|au|mid|midi|mpa|ra|ram|sln|csproj|vcxproj|vbproj|fsproj|fsxproj|pyproj|nupkg|vsix|vsct|vssettings|vsi|vstemplate|vsto)")
        # Exclude e.g. "package@v1.0.0" (It looks like an e-mail address but it is not. It is a package name with version)
        package_version_regex = re.compile(r".*@v\d+\.\d+\.\d+")
        # Exclude e.g. "xxx@example.com"
        example_email_regex = re.compile(r".*example.(com|org|net|cz|sk|eu|de|fr|uk|us|ca|au|jp|cn|ru|br|it|es|pl|nl|se|ch|at|be|dk|fi|no|pt|gr|hu|ie|lu|mx|nz|za|ar|cl|co|id|il|kr|my|ph|sg|th|tr|ua|vn)")
        
        extension_repositories = [name for name in os.listdir(REPOS_DIRECTORY) if name.startswith(extension_id)]

        repos_emails = set()
        for repository in extension_repositories:
            for path in Path(REPOS_DIRECTORY + "/" + repository).rglob('**/*'):
                if path.is_file():
                    with open(path, 'r', encoding="utf-8") as file:
                        try:
                            file_content = file.read()
                            repos_emails.update(set(email_regex.findall(file_content)))
                        except:
                            pass
        
        # Discard my git e-mail and others non-valid entries in the set of e-mails from the repositories
        MY_GIT_EMAIL = "martin.bedn20@gmail.com"
        repos_emails.discard(MY_GIT_EMAIL)
        repos_emails.discard("git@github.com")
        repos_emails = set(email for email in repos_emails if not re.fullmatch(filetypes_regex, email))
        repos_emails = set(email for email in repos_emails if not re.fullmatch(package_version_regex, email))
        repos_emails = set(email for email in repos_emails if not re.fullmatch(example_email_regex, email))
        
        # Write all information about extension to the CSV file
        git_links = ','.join(git_links)
        repos_emails = ','.join(repos_emails)
        f.write(name + ";" + extension_id + ";" + email + ";" + repos_emails + ";" + numberofusers + ";" + rating + ";" + numberofratings + ";" + git_links + "\n")



driver.quit()
