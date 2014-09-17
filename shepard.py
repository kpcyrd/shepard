#!/usr/bin/env python3
from colorama import Fore
import yaml
from subprocess import call, PIPE
from argparse import ArgumentParser
import sys

OK = Fore.GREEN + ' OK ' + Fore.RESET
FAIL = Fore.RED + 'FAIL' + Fore.RESET


def print_status(server, service, failure):
    status = OK if not failure else FAIL
    print('%-10s %-20s [%s]' % (server, service, status))


def run_exec_test(cmd):
    return call(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def run_all_tests(services):
    for service in services:
        if 'exec' in service:
            status = run_exec_test(service['exec'])
        print_status(service['host'], service['service'], status)

def main():
    args = parser.parse_args()

    with open(args.monitor) as f:
        services = yaml.load(f)

    run_all_tests(services)

parser = ArgumentParser()
parser.add_argument('monitor', help='yaml file for monitoring defintions')

if __name__ == '__main__':
    main()
