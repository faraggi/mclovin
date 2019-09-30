#!/usr/bin/env python3
import logging, json, os, sys

from github import Github
from github.GithubException import UnknownObjectException
from github.GithubException import GithubException

# database
# TODO
# import sqlite3
# from sqlite3 import Error

# multitreading:
# TODO
# import threading
import time
from datetime import datetime, timedelta

# debugging:
import pdb

# logging level. change to DEBUG, WARNING, INFO, etc for different levels
# logger = logging.getLogger('dev')
logging.getLogger().setLevel(logging.INFO)


# access tokens
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

g = Github(GITHUB_TOKEN)

# LICENSES = eval(open("licenses").read())

with open('github-projects-list.json') as complete_list: 
    real_data = json.load(complete_list)


# tmp or real data choice:
project_list = real_data['data']['allProjects']
# json_data = eval(test_data)
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
NO_LICENSE_COUNT = 0
LICENSE_COUNT = 0
RATE_LIMIT_MINIMUM = 30
ALL_LICENSES = []


def get_type(user):
    return user.type

def get_license_info(name, repo):
    try:
        license = repo.get_license()
        license = license.license
        license_info = (name, repo.name, license.spdx_id)
    except UnknownObjectException:
        logging.warning(f'UnknownObjectException - {name}: {repo.name} no license')
        license_info = (name, repo.name, 0)
    except GithubException:
        logging.warning(f'GithubException - {name}: {repo.name} UNACCESSIBLE!')
        license_info = (name, repo.name, "UNACCESSIBLE")
    return license_info

def count_licenses(name, license_info, ALL_LICENSES, LICENSE_COUNT, NO_LICENSE_COUNT, repo):
    # pdb.set_trace()
    try:
        license
    except NameError:
        ALL_LICENSES.append(license_info)
        NO_LICENSE_COUNT += 1
        logging.info(f'({name}, {repo.name}, 0)')
    else:
        ALL_LICENSES.append(license_info)
        LICENSE_COUNT += 1
        logging.info(license_info)

def loop_through_repos(name, repo_list):
    global NO_LICENSE_COUNT
    global LICENSE_COUNT
    global ALL_LICENSES

    for repo in repo_list:
        print(name, repo)
        license_info = get_license_info(name, repo)
        count_licenses(name, license_info, ALL_LICENSES, LICENSE_COUNT, NO_LICENSE_COUNT, repo)
        logging.info(LICENSE_COUNT)
        write_to_file(license_info)

def get_name(project):
    return project['name']

def write_to_file(item):
    item = ', '.join(map(str, item))
    with open('results.csv', 'a') as f:
        f.write(f'{item} \n')

def check_rate_limit():
    # rate limit for github API limits
    global RATE_LIMIT_MINIMUM
    if g.rate_limiting[0] < RATE_LIMIT_MINIMUM:
        # wait until limit_resettime if remaining calls are few
        while time.time() < g.rate_limiting_resettime:
            logging.warning('Waiting 2m for Rate Limit to top off...')
            logging.warning(f'Current rate_limiting: {g.rate_limiting}')
            readable_time = datetime.utcfromtimestamp(g.rate_limiting_resettime).strftime('%Y-%m-%d %H:%M:%S')
            logging.warning(f'Next reset at: {readable_time}')
            # readable_remaining_time = g.rate_limiting_resettime - time.time()
            # readable_remaining_time = datetime.utcfromtimestamp(readable_remaining_time).strftime('%Y-%m-%d %H:%M:%S')
            # logging.warning(f'Time Remaining: {readable_time}')
            time.sleep(120)

def main_loop():
    with open('results.csv', 'w') as f:
        # pdb.set_trace()
        check_rate_limit()
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
