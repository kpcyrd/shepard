#!/usr/bin/env python3
from colorama import Fore
import yaml
from subprocess import call, PIPE
import subprocess
import sys

OK = Fore.GREEN + ' OK ' + Fore.RESET
FAIL = Fore.RED + 'FAIL' + Fore.RESET


def print_status(server, service, failure):
    status = OK if not failure else FAIL
    print('%-10s %-20s [%s]' % (server, service, status))


def run_test(cmd):
    return call(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def main(settings_file):
    with open(settings_file) as f:
        settings = yaml.load(f)

    for service in settings:
        status = run_test(service['exec'])
        print_status(service['host'], service['service'], status)


def print_help():
    print('Usage: shepard <settings>')


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print_help()
