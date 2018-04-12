#!/usr/bin/env python

import boto3
ec2 = boto3.resource('ec2')

ids = ['i-0b05370429a6bfd56']

# Get status of instances
#for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
#    id    = status['InstanceId']
#    state = status['InstanceState']['Name']
#
#    print(id)
#    print(state)

# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
# instances = ec2.instances.filter(
#     Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
# for instance in instances:
#     print(instance.id, instance.instance_type)

# start/stop
#ec2.instances.filter(InstanceIds=ids).start()
#ec2.instances.filter(InstanceIds=ids).terminate()
