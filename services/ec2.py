from functionality.tools import Color, pp_json, status, percentage
from botocore.exceptions import ClientError
import boto3
import sys

class Ec2Manager:
    '''
    Houses all of the methods and attributes which are required to calculate and return the limits for
    On Demand, Spot Instances Requests and Default EC2 limits per account.
    '''
    def __init__(self, service):
        # print(service)
        self.service = service

    @staticmethod
    def describe_default_max_inst():
        client = boto3.client('ec2')
        try:
            response = client.describe_account_attributes(
                AttributeNames=['max-instances']
            )
            new_response = response['AccountAttributes'][0]['AttributeValues'][0]['AttributeValue']
            return new_response

        except ClientError as e:
            print(e)

    @staticmethod
    def ec2describer():
        client = boto3.client('ec2')
        inst_set = set()
        types_list= []

        try:
            response = client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name','Values': [
                            'running','stopped',],
                    },
                ],
            )

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instancetypes = instance['InstanceType']
                    types_list.append(str(instance['InstanceType']))

                inst_set.add(instance['InstanceType'])
                index_list = list(inst_set)

            return(index_list, types_list)

        except ClientError as e:
            print(e)

    def funct_executor(self):
        if self.service == 'OnDemand':
            print('{START}\r\n{text:^80}\r\n{END}'.format(text='~~ On Demand Instances ~~', START=Color.YELLOW, END=Color.END))
            result = self.ec2describer()
            index_list, types_list = [result[0], result[1]]

            for type_name in index_list:
                print("* On Demand Instance Type: {0}, Currently Active: {1}".format(type_name, types_list.count(type_name)))

            def_max = self.describe_default_max_inst()
            calc_percentage = percentage(len(types_list), def_max)
            print('\n{0}% Used by "On Demand" instances in this Region, Current On Demand Instance Total: {1}, Max On Demand Instances: {2} {3}'.format(calc_percentage, len(types_list), def_max, status(calc_percentage)))
