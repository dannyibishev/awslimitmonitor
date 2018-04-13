#!/usr/bin/env python
'''Limit Monitoring Script for AWS
Usage:
  awslimitmonitor  all | ec2 | rds | lb | asg

Options:
   -v --version     Show version.
   -h --help        Displays helpful options.

Author: Yordan Ibishev,  Contact details: dannyibishev@gmail.com
'''
import json
import boto3
from docopt import docopt
from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command
from services.ec2 import Ec2Manager
from services.asg import ASGManager

class Actions():

    def service_selector(arguments):
        typesList = {'lb':['LoadBalancer'] ,'asg':['AutoScalingGoups'] ,'ec2':['SpotRequests', 'OnDemand'] ,'rds':['RelationalDatabasesService']}

        if arguments['all']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving All Limits!', border=('=' * 80)))

        if arguments['ec2']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving EC2 Limits Only!', border=('=' * 80)))
            for service in typesList['ec2']:
                initiator = Ec2Manager(service)
                initiator.limitExecutor()

        elif arguments['rds']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving RDS Limits Only!', border=('=' * 80)))

        elif arguments['lb']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving Load Balancer Limits Only!', border=('=' * 80)))

        elif arguments['asg']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving ASG Limits Only!', border=('=' * 80)))
            for service in typesList['asg']:
                initiator = ASGManager(service)
                initiator.limitExecutor()

    # def getlicence():
    #     print('This is a future feature. To be implemented')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='LimitMonitor v0.1')
    Actions.service_selector(arguments)
