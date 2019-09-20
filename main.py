#!/usr/bin/env python3
import os, json, sys

import requests
from github import Github
from github.GithubException import UnknownObjectException
from gitterpy.client import GitterClient

# access tokens
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

g = Github(GITHUB_TOKEN)

ORGS = []
# PROJECTS = {}
PROJECTS = eval(open("test.json").read())
LICENSES = eval(open("licenses").read())

# test data and real data
with open('test.json') as test_json: 
    test_data = json.load(test_json) 

project_list = PROJECTS['data']['allProjects']

# print(project_list)
# print(len(project_list))

# cleaning up project list
for item in project_list:
    name = item['name']
    # print(name)
    # removing projects without github link
    if not item['githubLinks']:
        project_list.remove(item)

# for project in project_list:
#     # getting projects with multiple github links
#     if len(item['githubLinks']) > 1:
#         for link in item['githubLinks']:
#             project_list[name] = link

print(project_list)
print(len(project_list))
print('---')

for project in project_list:
    print(project)
    # print(project['githubLinks'])
    # try org
    try:
        name = g.get_organization(project['name'])
    except UnknownObjectException:
        # try user
        try:
            name = g.get_repo(project['name'])
        except UnknownObjectException:
            # try repo
            try:
                name = g.get_user(project['name'])
                # print(f"{name} is USER!")
            except UnknownObjectException:
                # print(name)
                print("UnknownObjectException")
                # print("Isn't any type.")
                project_list.remove(project)

print('---')
print(project_list)
print(len(project_list))

# for i, k in json_list.items():
#     print(i, "-", k)

# print(json_list)

# cleaning up project list
# json_list = {}
# for item in (real_data or test_data_projects):
#     name = item['name']
#     # print(name)
#     # getting projects with multiple github links
#     if len(item['githubLinks']) > 1:
#         for link in item['githubLinks']:
#             json_list[name] = link
# 
#     # removing projects without github link
#     elif item['githubLinks']:
#         json_list[item['name']] = item['githubLinks']

# for i, k in json_list.items():
#     print(i, "-", k)
# 
# print(json_list)



# print("+++++++++++++++++++++++++++++++")
# print("+++++++++++++++++++++++++++++++")
# 
# # repo
# repo_name = test_data['data']['allProjects'][0]['name']
# repo = g.get_repo(repo_name)
