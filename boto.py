#!/usr/bin/env python

import sys
import boto3
from pprint import pprint
from botocore.exceptions import ClientError

ids = ['i-02889f94b07c5b535']

ec2b = boto3.client('ec2')
response = ec2b.describe_instances()

def describe_keys():
    response = ec2b.describe_key_pairs()
    pprint(response)

def create_key_pair():
    ec2 = boto3.client('ec2')
    response = ec2b.create_key_pair(KeyName='KEY_PAIR_NAME')
    print(response)

def describe_ec2_simple():
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(instance["InstanceId"])
            print(instance['State']['Name'])

# start/stop
#ec2.instances.filter(InstanceIds=ids).start()
# ec2.stop_instances(InstanceIds=['i-02889f94b07c5b535'], DryRun=False)
# ec2.instances.filter(InstanceIds=ids).terminate()

def start_instances(ids):

    print('Starting instances')
    try:
        ec2b.start_instances(InstanceIds=ids, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    ec2b.start_instances(InstanceIds=ids, DryRun=False)

def stop_instances(ids):

    print('Stopping instances')
    try:
        ec2b.stop_instances(InstanceIds=ids, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    ec2b.stop_instances(InstanceIds=ids, DryRun=False)

#start_instances(ids)
#stop_instances(ids)
describe_ec2_simple()
