import boto3
import sys
from botocore.exceptions import ClientError
from functionality.tools import Color, pp_json, status, percentage


class Ec2Manager:
    """
    Houses all of the methods and attributes which are required to calculate and return the limits for
    On Demand, Spot Instances Requests and Default EC2 limits per account.
    """
    def __init__(self, service):
        """ this class will need to be initialised with the correct service before using any other method/function within the class."""
        self.service = service

    @staticmethod
    def describe_max_inst():
        """ Returns the account max instances limit. (default is 1000) """
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
    def spot_requests_describer():
        """
        Dynamically retrieves all spot requests in a started | stopped state. (Will need to add the cancelled state in the future as it counts towards the limit)
        """
        client = boto3.client('ec2')
        types_list= []
        inst_set = set()
        try:
            response = client.describe_spot_instance_requests(
                Filters=[
                    {
                        'Name': 'state',
                        'Values': ['active', 'open']
                    }
                ]
            )

            for request in response['SpotInstanceRequests']:
                instance_types = request['LaunchSpecification']['InstanceType']

                #Creates a list of all the types.
                types_list.append(request['LaunchSpecification']['InstanceType'])

                #Sets indexes to choose from.
                inst_set.add(instance_types)
                index_list = list(inst_set)

            try:
                for i in index_list:
                    print("* Spot Instance Type: {0}, Currently Active or Open: {1}".format(i, types_list.count(i)))
                total_count = len(types_list)
                print("\r\n* Total Active Spot instances in this Region: {0}".format(total_count))
            except UnboundLocalError as e:
                print("\r\n* Total Active Spot instances in this Region: {0} {1}".format("0", status("0")))

        except ClientError as e:
            print("Nope")

    @staticmethod
    def ec2describer():
        """
        Dynamically retrieves all instances in a started | stopped state.
        An index_list and types_list is returned for data manipulation outside the function.
        """
        client = boto3.client('ec2')
        inst_set = set()
        types_list= []

        try:
            response = client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name', 'Values': ['running', 'stopped']
                    }
                ]
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
        """
        Triggers the appropiate functions depending on what service is used.

        Services supported:
        - OnDemand
        - SpotRequests - To Implement
        - ReservedInstances - Future Implementation. Not Yet Set Up!
        """
        if self.service == 'OnDemand':
            print('{START}\r\n{text:^80}\r\n{END}'.format(text='~~ On Demand Instances ~~', START=Color.YELLOW, END=Color.END))
            result = self.ec2describer()

            if result != None:
                index_list, types_list = [result[0], result[1]]

                for type_name in index_list:
                    print("* On Demand Instance Type: {0}, Currently Active: {1}".format(type_name, types_list.count(type_name)))

            def_max = self.describe_max_inst()
            calc_percentage = percentage(len(types_list), def_max)
            print('\r\n* {0}% Used by "On Demand" instances in this Region, Current On Demand Instance Total: {1}, Max On Demand Instances: {2} {3}'.format(calc_percentage, len(types_list), def_max, status(calc_percentage)))

        elif self.service == 'SpotRequests':
            print('{START}\r\n{text:^80}\r\n{END}'.format(text='~~ Spot Instance Requests ~~', START=Color.YELLOW, END=Color.END))
            self.spot_requests_describer()
