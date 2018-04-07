#!/usr/bin/env python
'''Limit Monitoring Script for AWS
Usage:
  awslimitmonitor  all|ec2|rds|load_balancer|asg

Options:
  -h --help        Show this screen.
  --version -v     Show version.
'''
from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command
from docopt import docopt
from services.ec2 import Ec2Manager
import json
import boto3

class Actions():
    border = ('=' * 80)
    # def __init__(self,border):
    #
    #     self.border = border
    # def services_list(self):
    #     print(hello)
    #
    #     self.load_balancer =
    #     self.ec2 = ['']
    #     self.asg =
    #     self.rds =
    #     self.other =

    def service_selector(arguments):
        # type_lists = {'load_balancer_funct':['describe_load_balancers_alb', 'describe_load_balancers_elb' ,'describe_account_limits_alb'] ,'asg_funct':['describe_account_limits_asg'] ,'ec2_funct':['describe_spot_instance_requests' ,'describe_default_max_inst' ,'ec2_describe_instances'] ,'rds_funct':['describe_account_rds']}
        services = ['OnDemand', 'SpotRequests', 'Defaults']

        if arguments['all']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving All Limits!', border=('=' * 80)))
            # for functions in lists.values():
            #     for limits in functions:
            #         limits()
            #
        if arguments['ec2']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving EC2 Limits Only!', border=('=' * 80)))
            for service in services:
                initiator = Ec2Manager(service)
                initiator.funct_executor()

        elif arguments['rds']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving RDS Limits Only!', border=('=' * 80)))
            # for limits in lists.values()[2]:
            #     limits()
            #
        elif arguments['load_balancer']:
            print('{border}\r\n{text:^80}\r\n{border}'.format(text='Retrieving Load Balancer Limits Only!', border=('=' * 80)))
            # describe_load_balancers_alb()
            # describe_load_balancers_elb()
            # describe_account_limits_alb()
        # elif arguments['asg']:
        #     print('-' * 50 + '\n' + ' ' * 11 + 'Retrieving ASG Limits Only!\n' + '-' * 50)
        #     for limits in lists.values()[1]:
        #         limits()

    # def getlicence():
    #     print('This Needs finishing off')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='LimitMonitor v0.1')
    Actions.service_selector(arguments)
