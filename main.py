#!/usr/bin/env python3
import os, json, sys

# database
import sqlite3
from sqlite3 import Error


import pprint
import requests
from github import Github
from github.GithubException import UnknownObjectException
from gitterpy.client import GitterClient

# multitreading:
import threading
import time

# debugging:
import pdb

# access tokens
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

g = Github(GITHUB_TOKEN)

PROJECTS = eval(open("github-projects-list.json").read())
LICENSES = eval(open("licenses").read())

# test data and real data
with open('github-projects-list.json') as complete_list: 
    real_data = json.load(complete_list)

#db connection
def create_connection(db_file):
    """
    create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


test_data = '''
{
  "data": {
    "allProjects": [
      {
        "githubLinks": [
          "https://github.com/0chain"
        ],
        "name": "0chain"
      },
      {
        "githubLinks": [
          "https://github.com/0xproject"
        ],
        "name": "0x"
      },
      {
        "githubLinks": [
          "https://github.com/0xbitcoin"
        ],
        "name": "0xBitcoin"
      },
      {
        "githubLinks": [
          "https://github.com/0xcert"
        ],
        "name": "0xcert Protocol"
      },
      {
        "githubLinks": [
          "https://github.com/1irstcoin"
        ],
        "name": "1irstcoin"
      },
      {
        "githubLinks": [],
        "name": "1SG"
      },
      {
        "githubLinks": [
          "https://github.com/1world-online"
        ],
        "name": "1World"
      },
      {
        "githubLinks": [
          "https://github.com/aave",
          "https://github.com/ETHLend"
        ],
        "name": "Aave"
      }
      ]
    }
}
''' 
# test_data = '''
# {
#   "data": {
#     "allProjects": [
#       {
#         "githubLinks": [
#           "https://github.com/0xproject"
#         ],
#         "name": "0x"
#       }
#       ]
#     }
# }
# ''' 

json_data = eval(test_data)
# pprint.pprint(test_data)

# tmp or real data choice:
project_list = real_data['data']['allProjects']
# project_list = json_data['data']['allProjects']

# print(project_list)
# print(len(project_list))

def clean_up(list):
    # cleaning up project list
    for item in list:
        name = item['name']
        # removing projects without github link
        if not item['githubLinks']:
            list.remove(item)
    return list

# print(project_list)
project_list = clean_up(project_list)


license_count = 0
no_license_count = 0
all_licesnses = []
print(license_count)

# number_loop = 1
# current_loop = 1
# while current_loop < 3:
#     filename = 'results{number_loop}.text'
#     with open(filename, 'w') as f:
#         for item in all_licesnses:
#             f.write(f"{item}\n")
#     current_loop += 1
# number_loop += 1

# with open(filename, 'w') as f:
#     for item in all_licesnses:
#         f.write(f"{item}\n")

for project in project_list:
    name = project['name']
    print(name)
    # try org
    try:
        org = g.get_organization(project['name'])
        repos = org.get_repos()
        for repo in repos:
            try:
                license = repo.get_license()
                license = repo.get_license().license
                all_licesnses.append((name, repo.name, license.spdx_id))
                license_count += 1
                print(license_count)
                print((name, repo.name, license.spdx_id))
            except UnknownObjectException:
                # print('no license found')
                all_licesnses.append((name, repo.name, 0))
                no_license_count += 1
                print(license_count)
                print((name, repo.name, 0))
                
    except UnknownObjectException:
        # pdb.set_trace()
        print('not org')
        # try user
        try:
            user = g.get_user(project['name'])
            repos = user.get_repos()
            for repo in repos:
                try:
                    license = repo.get_license()
                    license = repo.get_license().license
                    all_licesnses.append((name, repo.name, license.spdx_id))
                    license_count += 1
                    print(license_count)
                    print((name, repo.name, license.spdx_id))
                except UnknownObjectException:
                    # print('no license found')
                    all_licesnses.append((name, repo.name, 0))
                    no_license_count += 1
                    print(license_count)
                    print((name, repo.name, 0))
            
        except UnknownObjectException:
            # try repo
            print('not user')
            try:
                repo = g.get_repo(project['name'])
                license = repo.get_license()
                license = repo.get_license().license
                all_licesnses.append((name, repo.name, license.spdx_id))
                license_count += 1
                print(license_count)
                print((name, repo.name, license.spdx_id))


            except UnknownObjectException:
                print("+++++")
                print("UnknownObjectException", name)
                print(g.get_user())
                print("+++++")

# FIN?
print("=================")
print(license_count)
print(no_license_count)

pprint.pprint(all_licesnses)




############################
############################
############################
############################
sys.exit()


results = {}

def is_org(org_name):
    try:
        org = g.get_organization(org_name)
        return org
    except UnknownObjectException:
        # print("not org")
        pass

def is_user(user_name):
    try:
        user = g.get_user(user_name)
        return user
    except UnknownObjectException:
        # print("not user")
        pass

def is_repo(repo_name):
    try:
        repo = g.get_repo(project['name'])
        return repo
    except UnknownObjectException:
        # print("Not repo")
        pass

def loop_through_repos(repo_list):
    for i in repo_list:
        print(i)
        # print(i.name)

def get_type(name):
    if is_org(name):
        return org
    # elif is 

# for project in project_list:
#     name = project['name']
#     print(name)
    
    
    # get_type(name)
    # org = is_org(name):
    #     loop_through_repos()
    #     print("IS ORG")
    # elif is_user(name):
    #     print("IS USER")
    # elif is_repo(name):
    #     print("IS REPO")


for project in project_list:
    name = project['name'] 
    # print("PROJECT NAME:")
    print(name)
    # if is_org(name):
    #     print("IS ORG")
    # else:
    #     print("ISN'T ORG")
    ##############
    # try org
    try:
        org = g.get_organization('Aave')
        # org = g.get_organization(project['name'])
        repos = org.get_repos()
        for repo in repos:
            # print("REPO NAME:")
            # print(repo.name)
            license = repo.get_license()
            license = repo.get_license().license
            all_licesnses.append((repo.name, license))
    except UnknownObjectException:
        # try user
        try:
            repo = g.get_repo(project['name'])
        except UnknownObjectException:
            # try repo
            try:
                user = g.get_user(project['name'])
                # print(f"{name} is USER!")
            except UnknownObjectException:
                # print(name)
                print("UnknownObjectException")
                # print("Isn't any type.")
                project_list.remove(project)
print(all_licesnses)

# print('---')
# print(project_list)
# print(len(project_list))

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
