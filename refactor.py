#!/usr/bin/env python3
import logging, json, os, sys

from github import Github
from github.GithubException import UnknownObjectException

# database
# TODO
# import sqlite3
# from sqlite3 import Error

# multitreading:
# TODO
# import threading
# import time

# debugging:
# import pdb

# logging level. change to DEBUG, WARNING, INFO, etc for different levels
# logger = logging.getLogger('dev')
logging.getLogger().setLevel(logging.INFO)


# access tokens
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

g = Github(GITHUB_TOKEN)

# LICENSES = eval(open("licenses").read())

with open('github-projects-list.json') as complete_list: 
    real_data = json.load(complete_list)

json_data = eval(test_data)

# tmp or real data choice:
project_list = real_data['data']['allProjects']
# project_list = json_data['data']['allProjects']

def clean_up(list):
    # cleaning up project list
    for item in list:
        name = item['name']
        # removing projects without github link
        if not item['githubLinks']:
            list.remove(item)
    return list

# print(project_list)
PROJECT_LIST = clean_up(project_list)


def get_type(user):
    return user.type

def loop_through_repos(name, repo_list):
    for repo in repo_list:
        try:
            license = repo.get_license()
            license = repo.get_license().license
            license_info = (name, repo.name, license.spdx_id)
        except UnknownObjectException:
            license_info = (name, repo.name, 0)
        if license:
            ALL_LICENSES.append(license_info)
            LICENSE_COUNT += 1
            logging.info(f'({name}, {repo.name}, {license.spdx_id})')
        else:
            ALL_LICENSES.append(license_info)
            NO_LICENSE_COUNT += 1
            logging.info(f'({name}, {repo.name}, 0)')
        logging.info(LICENSE_COUNT)
        write_to_file(license_info)

def get_name(project):
    return project['name']

def write_to_file(item):
    with open('results.csv', 'a') as f:
        f.write(f'{item} \n')

def main_loop():
    with open('results.csv', 'w') as f:
        # pdb.set_trace()
        for project in PROJECT_LIST:
            name = get_name(project)
            logging.info(f'Name: {name}')
            try:
                user = g.get_user(name)
            except:
                continue
            
            # type = get_type(user)  # get type (not used for now)
            # logging.info(f'Type: {type}')
            
            # get repos and loop over them
            repos = user.get_repos()
            loop_through_repos(name, repos)
            

if __name__ == "__main__":
    main_loop()
