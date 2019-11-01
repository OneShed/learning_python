import json
import os
import sys


def json_pprint( dict):
    jsond = json.dumps(dict, indent=4, sort_keys=False)
    print(jsond)



# Statuses are returned in reverse chronological order. The first state in
# list will be the latest one # https://developer.github.com/v3/repos/statees/#list-statees-for-a-specific-ref


context = "Start App Server"
data_file = "statuses.txt"
json_template = open(data_file).read()

#!/usr/bin/python
context = "Start App Server"

import json
import sys

def get_state(context):
    states_json = json.loads(json_template)
    for state_json in states_json:
        if state_json['context'] == context:
            return state_json['state']
    return 'not defined'

print(get_state(context))
import json
import sys

def get_state(context):
    states_json = json.loads(json_template)
    for state_json in states_json:
        if state_json['context'] == context:
            return state_json['state']
    return 'not defined'

print(get_state(context))




