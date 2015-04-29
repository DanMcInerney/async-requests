#!/usr/bin/python2

#This must be one of the first imports or else we get threading error on completion
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
from gevent import joinall
import requests
import argparse

def parse_args():
    ''' Create the arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--connections", default=10, type=int,
                        help="Set how many concurrent connections to use")
    return parser.parse_args()

def concurrency(urls):
    ''' Open all the greenlet threads '''
    args = parse_args()
    pool = Pool(args.connections)
    jobs = [pool.spawn(make_request, url) for url in urls]
    return joinall(jobs)

def make_request(url):
    ''' Make request to url '''
    ua = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}

    try:
        resp = requests.get(url, timeout=10, headers = ua)
    except Exception as e:
        print '[-] {}'.format(url)
        return

    # Perform some action on the response
    do_something_with_resp(resp)

def do_something_with_resp(resp):
    ''' Perform some action on the response '''
    # Remove whitespace from beginning and end of html
    html = resp.text.strip()
    first_line = html.split('\n')[0]
    print '[*] {}'.format(first_line)

def main():
    urls = ['http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/',
            'http://securityweekly.com/']
    concurrency(urls)

main()
