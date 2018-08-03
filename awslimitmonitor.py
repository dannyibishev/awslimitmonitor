#!/usr/bin/env python3
'''Limit Monitoring Script for AWS
Usage:
  awslimitmonitor  all | ec2 | rds | lb | asg

Options:
   -v --version     Show version.
   -h --help        Displays helpful options.

Author: Yordan Ibishev,  Contact details: dannyibishev@gmail.com
'''
import boto3
from docopt import docopt
from services.ec2 import Ec2Manager
from services.asg import ASGManager
from services.rds import RDSManager
from services.lb import LBManager

class Actions(object):
    """
    Uses arguments passed from __main__ to perform actions related to
    the service

    Takes the following Arguments
    - 'all'
    - 'asg'
    - 'ec2'
    - 'rds'
    - 'lb'
    """
    def __init__(self, argument):
        self.argument = argument
        # self.typesList = typesList

    def service_selector(self):
        typesList = {'lb': ['LoadBalancer', 'TargetGroup'],
                     'asg': ['AutoScalingGoups'],
                     'ec2': ['SpotRequests', 'OnDemand', 'EBS'],
                     'rds': ['RelationalDatabasesService']}

        if self.argument['all']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(
                text='Retrieving All Limits!',
                border=('=' * 80)
                ))
        elif self.argument['ec2']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(
                text='Retrieving EC2 Limits Only!',
                border=('=' * 80)
                ))

            for service in typesList['ec2']:
                initiator = Ec2Manager(
                    service,
                    client=boto3.client('ec2')
                    )

                initiator.limit_executor()

        elif self.argument['rds']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(
                text='Retrieving RDS Limits Only!',
                border=('=' * 80)
                ))

            for service in typesList['rds']:
                initiator = RDSManager(
                    service,
                    client=boto3.client('rds')
                    )

                initiator.limit_executor()

        elif self.argument['lb']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(
                text='Retrieving Load Balancing Limits Only!',
                border=('=' * 80)
                ))

            for service in typesList['lb']:
                initiator = LBManager(
                    service,
                    albclient=boto3.client('elbv2'),
                    elbclient=boto3.client('elb')
                    )

                initiator.limit_executor()

        elif self.argument['asg']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(
                text='Retrieving ASG Limits Only!',
                border=('=' * 80)
                ))

            for service in typesList['asg']:
                initiator = ASGManager(
                    service,
                    client=boto3.client('autoscaling')
                    )

                initiator.limit_executor()

    # def getlicence():
    #     print('This is a future feature. To be implemented')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='LimitMonitor v0.1')
    Actions(arguments).service_selector()

    Actions(argume)
