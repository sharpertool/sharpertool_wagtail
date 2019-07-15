#!/usr/bin/env python

import argparse

import json
import sys
from os import environ

import requests

from cilib.getip import get_my_ip


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('firewall',
                        help='ID of the Digital Ocean Firewall to add rules to')
    parser.add_argument('--remove',
                        action='store_true',
                        help="Specify remove to remove the rule, otherwise will add rule")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    token = environ['DIGITALOCEAN_API_TOKEN']

    myip = get_my_ip()

    if myip is None:
        print("Failed to get my  ip address. Cannot proceed")
        sys.exit(2)

    print(f"Adding access to port 22 to {myip}")
    rules = {
        "inbound_rules": [
            {
                "protocol": "tcp",
                "ports": 22,
                "sources": {
                    "addresses": [
                        myip
                    ]
                }
            }
        ]
    }

    rfunc = requests.post
    if args.remove:
        rfunc = requests.delete

    res = rfunc(f"https://api.digitalocean.com/v2/firewalls/{args.firewall}/rules",
                headers={
                    'content-type': 'application/json',
                    'Authorization': f"Bearer {token}",
                },
                data=json.dumps(rules))

    print(f"Response code {res.status_code}")

    if res.status_code == 204:
        if args.remove:
            print("Firewall Rules removed")
        else:
            print("Firewall Rules Added")
    else:
        print("Failed to create new firewall. Please review issues")


if __name__ == "__main__":
    main()
