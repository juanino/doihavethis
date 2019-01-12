#!/usr/bin/env python3
import yaml
import pprint
import json
import requests
import sys

try:
    message = sys.argv[1]
except:
    print("no message passed, usage: ./send_slack blah")
    sys.exit(1)

# debug
pp = pprint.PrettyPrinter(indent=4)

# read yaml
with open('/etc/diht_integrations.yaml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def dump_config(cfg):
    pp.pprint(cfg)

dump_config(cfg)

url = cfg['slack']['webhook']
do_slack = cfg['slack']['enable']

print("----------")
pp.pprint(url)
print("----------")
pp.pprint(do_slack)


if (len(message) > 0):
    if do_slack:
        data = {
                'text': message
        }
        print("the data is " )
        print(data)
        response = requests.post(
            url, data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
