#!/usr/bin/python3
import argparse
import requests


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


msg = '''{}usage: subchk.py [-h] [-s SUBDOMAINS] [-t TIMEOUT] [-o OUTPUT]

SubDomain Checker Http & Https

optional arguments:
  -h, --help                        show this help message and exit
  -s SUBDOMAINS, --subdomains       Path Subdomains File
                        
  -t TIMEOUT, --timeout Timeout     Default: 1 Second
  -o OUTPUT, --output  Path Save    Result Default:result.txt

{}|#| https://fb.com/linux.2.0.1.4 |#|
'''.format(Colors.OKGREEN, Colors.WARNING)
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomains', help='path subdomains')
parser.add_argument('-t', '--timeout', type=int,default=1)
parser.add_argument('-o', '--output',default='result.txt')
argv = parser.parse_args()

if not argv.subdomains:
    print(msg)
    exit()

subdomains = []
live = []

with open(argv.subdomains, 'r') as subs:
    for sub in subs.readlines():
        subdomains.append('https://' + sub)
        subdomains.append('http://' + sub)
print('SubDomain Count:', len(subdomains))

for url in subdomains:
    try:
        url = url.rstrip('\n')
        r = requests.get(url, allow_redirects=False,timeout=argv.timeout)
        if r.status_code == 200:
            print(Colors.OKGREEN + url)
            save = open(argv.output, 'a+')
            save.write(url + '\n')
            save.close()
            live.append(url)
        else:
            print(Colors.FAIL + url, '[Not Working]')
    except:
        print(Colors.FAIL + url, '[Timeout]')

print(Colors.OKBLUE, 'Live SubDomain:', len(live))
