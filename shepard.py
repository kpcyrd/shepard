#!/usr/bin/env python3
from colorama import Fore
import yaml
from subprocess import call, PIPE
from argparse import ArgumentParser
import requests
import time
import sys

OK = Fore.GREEN + ' OK ' + Fore.RESET
FAIL = Fore.RED + 'FAIL' + Fore.RESET

SUCCESS = 0
FAILURE = 1

def print_status(server, service, failure):
    status = OK if not failure else FAIL
    print('%-15s %-45s [%s]' % (server, service, status))


def run_exec_test(cmd):
    return call(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def run_http_test(http):
    try:
        body = requests.get(http['url'])
        if 'contains' in http and http['contains'] not in body.text:
            return FAILURE
        return SUCCESS
    except:
        return FAILURE


def run_all_tests(services):
    for service in services:
        if 'exec' in service:
            status = run_exec_test(service['exec'])
        elif 'http' in service:
            status = run_http_test(service['http'])
        print_status(service['host'], service['service'], status)


def run_all_tests_forever(services, interval):
    try:
        while True:
            run_all_tests(services)
            print('~' * 25)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


def main():
    args = parser.parse_args()

    with open(args.monitor) as f:
        services = yaml.load(f)

    if args.interval is not None:
        run_all_tests_forever(services, args.interval)
    else:
        run_all_tests(services)

parser = ArgumentParser()
parser.add_argument('monitor', help='yaml file for monitoring defintions')
parser.add_argument('-i', '--interval', type=int, help='repeat tests in interval x')

if __name__ == '__main__':
    main()
