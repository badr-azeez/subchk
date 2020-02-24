#!/usr/bin/python3

from multiprocessing.dummy import Pool as ThreadPool
import argparse
import requests
import sys
import os


class Colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


subdomains_list = []
live = []
nameScript = os.path.basename(__file__)

if sys.version_info[0] < 3:
    print(Colors.WARNING + "Must be using Python 3")
    sys.exit()
logo = '''{}
                          o                       o           o      
                         <|>                     <|>         <|>     
                         / >                     / >         / \     
     __o__   o       o   \o__ __o         __o__  \o__ __o    \o/  o/ 
    />  \   <|>     <|>   |     v\       />  \    |     v\    |  /v  
    \o      < >     < >  / \     <\    o/        / \     <\  / \/>   
     v\      |       |   \o/      /   <|         \o/     o/  \o/\o   
      <\     o       o    |      o     \\         |     <|    |  v\  
 _\o__</     <\__ __/>   / \  __/>      _\o__</  / \    / \  / \  <\ 
                    
                   |#| Wilaia Shield Team |#|
                   {}B{}adr {}A{}zeez fb.com/linux.2.0.1.4
                   
'''.format(Colors.BOLD + Colors.OKBLUE, Colors.FAIL, Colors.OKBLUE, Colors.BOLD + Colors.FAIL, Colors.OKBLUE)
msg = logo + '''{}usage: {} [-h] -s SUBDOMAINS [-t Threads] [-o OUTPUT]

optional arguments:
  -h, --help                        show this help message and exit
  -s SUBDOMAINS, --subdomains       Path Sub-domains File

  -t Threads, --threads Threads     Default: 3 Thread
  -o OUTPUT, --output  Path Save    Default:result.txt
'''.format(Colors.OKBLUE, nameScript)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-s', '--subdomains')
parser.add_argument('-t', '--threads', type=int, default=3)
parser.add_argument('-o', '--output', default='result.txt')
parser.add_argument('-h', '--help', action='store_true', default=False)
argv = parser.parse_args()

if argv.subdomains and not os.path.isfile(argv.subdomains):
    print(Colors.WARNING + 'No such file or directory' + Colors.BOLD, argv.subdomains)
    exit()

if not argv.subdomains or argv.help:
    print(msg)
    sys.exit()

if argv.help:
    print(msg)
    sys.exit()


def get_urls(subdomains):
    with open(subdomains, 'r') as subs:
        for sub in subs.readlines():
            sub = sub.rstrip()
            if not sub.startswith('http'):
                subdomains_list.append('http://' + sub)
                subdomains_list.append('https://' + sub)
            else:
                subdomains_list.append(sub)


get_urls(argv.subdomains)


def get_status(url):
    with open(argv.output, 'a+') as save:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200 and r.history:
                if url not in live:
                    live.append(r.url)
                    save.write(r.url + '\n')
                print(Colors.WARNING + Colors.BOLD + '|' + str(
                    r.history[0].status_code) + '| ' + Colors.ENDC + Colors.WARNING + url, '| Redirect =>',
                      Colors.OKGREEN + r.url, '|', Colors.OKBLUE + '(Redirect Saved)')
            elif r.status_code == 200:
                if r.url not in live:
                    live.append(r.url)
                    save.write(r.url + '\n')
                print(Colors.OKGREEN + Colors.BOLD + '|' + str(
                    r.status_code) + '| ' + Colors.ENDC + Colors.OKGREEN + r.url, Colors.OKBLUE + '(Saved)')
            else:
                print(Colors.FAIL + Colors.BOLD + url, '[Not Work]')
        except:
            print(Colors.FAIL + Colors.BOLD + url, '[Not Work]')


def liven():
    print(Colors.OKBLUE + '\nLive SubDomain:', sum(1 for line in open(argv.output)))


if __name__ == "__main__":
    try:
        print(logo)
        pool = ThreadPool(argv.threads)
        results = pool.map(get_status, subdomains_list)
        pool.close()
        pool.join()
        liven()
    except KeyboardInterrupt:
        liven()
        sys.exit('\nBye')
