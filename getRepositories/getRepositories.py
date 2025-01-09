#!/usr/bin/env python3

# Author: Martin Bednar (2024)

from git import Repo
from datetime import datetime
import os

already_downloaded_repos = [name.split(' ')[0]+"_"+name.split(' ')[2] for  name in os.listdir("./repos")]
print("Already downloaded repositories: " + str(already_downloaded_repos))

header_line = False

with open("PrivacyAndSecurityExtensions.csv", "r", encoding="utf-8") as f:
    for line in f:
        if not header_line:
            header_line = line.rstrip().split(';')
            continue
        line = line.rstrip().split(';')
        if len(line) != len(header_line):
            print("Error parsing line Maybe empty line? Line: " + str(line))
            continue
        try:
            extensionId = line[1]
            repos_urls = []
            if line[6] != "":
                repos_urls = line[6].rstrip().split(',')
        except:
            print("Error parsing line: " + str(line))
            continue
        for repo_url in repos_urls:
            # Clone the repository if it is not a bitbucket repository
            # Bitbucket repositories are not cloned because they require authentication
            # and the credentials are not provided in this script
            if "bitbucket" in repo_url:
                print("Bitbucket repository: " + repo_url)
                print("Repository not cloned: " + extensionId+"_"+repo_url.split('/')[-1] + " (" + repo_url + ")")
                print("Bitbucket repositories are not cloned because they require authentication and the credentials are not provided in this script")
                continue
            print("Cloning repository: " + extensionId+"_"+repo_url.split('/')[-1])
            if extensionId+"_"+repo_url.split('/')[-1] in already_downloaded_repos:
                print("Repository already downloaded: " + extensionId+"_"+repo_url.split('/')[-1] + " (" + repo_url + ")")
                continue
            try:
                repo = Repo.clone_from(repo_url, "./repos/" + extensionId + " - " + repo_url.split('/')[-1] + " - " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            except:
                print("Error cloning repository: " + repo_url)
                continue

