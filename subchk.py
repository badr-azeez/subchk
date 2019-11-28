#!/usr/bin/python3
import argparse
import requests
import sys


class Colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


if sys.version_info[0] < 3:
    print(Colors.WARNING + "Must be using Python 3")
    sys.exit()

msg = '''{}usage: {} [-h] -s SUBDOMAINS [-t TIMEOUT] [-o OUTPUT]

SubDomain Checker Http & Https

optional arguments:
  -h, --help                        show this help message and exit
  -s SUBDOMAINS, --subdomains       Path Subdomains File
                        
  -t TIMEOUT, --timeout Timeout     Default: 1 Second
  -o OUTPUT, --output  Path Save    Result Default:result.txt

{}|#| https://fb.com/linux.2.0.1.4 |#|
'''.format(Colors.WARNING, sys.argv[0], Colors.BOLD + Colors.OKGREEN)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-s', '--subdomains')
parser.add_argument('-t', '--timeout', type=int, default=3)
parser.add_argument('-o', '--output', default='result.txt')
parser.add_argument('-h', '--help', action='store_true', default=False)
argv = parser.parse_args()

if not argv.subdomains or argv.help:
    print(msg)
    sys.exit()
if argv.help:
    print(msg)
    sys.exit()

subdomains_list = []
live = []


def get_urls(subdomains):
    with open(subdomains, 'r') as subs:
        for sub in subs.readlines():
            if not sub.startswith('http') and not sub.startswith('https'):
                subdomains_list.append('http://' + sub)
                subdomains_list.append('https://' + sub)
            else:
                subdomains_list.append(sub)

    print('SubDomain Count:', len(subdomains_list))


def check_url(url):
    url = url.rstrip('\n')
    try:
        r = requests.get(url, allow_redirects=False, timeout=argv.timeout)
        if r.status_code == 200:
            print(Colors.OKGREEN + Colors.BOLD + '|' + str(r.status_code) + '| ' + Colors.ENDC + url)
            save = open(argv.output, 'a+')
            save.write(url + '\n')
            save.close()
            live.append(url)
        elif r.status_code >= 300 or r.status_code < 400:
            print(Colors.FAIL + Colors.BOLD + '|' + str(r.status_code) + '| ' + Colors.ENDC + url, '[Not Working]')
    except KeyboardInterrupt:
        sys.exit('\nBye')
    except:
        print(Colors.FAIL + Colors.BOLD + url, '[Timeout]')


get_urls(argv.subdomains)

for url in subdomains_list:
    check_url(url)

print(Colors.OKBLUE, 'Live SubDomain:', len(live))
