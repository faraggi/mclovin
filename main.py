#!/usr/bin/env python3
import os, json

import requests
from github import Github
from github.GithubException import UnknownObjectException
from gitterpy.client import GitterClient

# access tokens
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']


# test data
with open('test.json') as test_json: 
    test_data = json.load(test_json) 

test_data_projects = test_data['data']['allProjects']


g = Github(GITHUB_TOKEN)

# for repo in g.get_user().get_repos():
project_list = []
for project in test_data_projects:
    print(project)
    if len(project['githubLinks']) > 0:
        project_list.append(project)

for project in test_data_projects:
    print(project)
    # print(project['githubLinks'])
    # try org
    try:
        name = g.get_organization(project['name'])
        # print(f"{name} is ORG!")
    except UnknownObjectException:
        # print("UnknownObjectException")
        pass
    
    # try project
    # try:
    #     name = g.get_project(project['name'])
    #     print(f"{name} is PROJECT!")
    # except UnknownObjectException:
    #     print("NOT PROJECT")

    # try user
    try:
        name = g.get_user(project['name'])
        # print(f"{name} is USER!")
    except UnknownObjectException:
        # print("UnknownObjectException")
        pass

# print("+++++++++++++++++++++++++++++++")
# print("+++++++++++++++++++++++++++++++")
# 
# # repo
# repo_name = test_data['data']['allProjects'][0]['name']
# repo = g.get_repo(repo_name)
