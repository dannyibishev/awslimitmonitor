"""
The EC2 Module, awslimitmonitor imports this to calculate
all EC2 limits.
"""
from botocore.exceptions import ClientError
from functionality.tools import Color, pp_json, status, percentage
from networking.connections import RequestExpired


class Ec2Manager:
    """
    Houses all of the methods and attributes which are required to
    calculate and return the limits for On Demand, Spot Instance
    Requests and Default EC2 limits per account.
    """
    def __init__(self, service, client) -> str:
        """
        this class will need to be initialised with the correct service
        before using any other method/function within the class.
        """
        self.service = service
        self.client = client


    @staticmethod
    def describe_max_inst(client) -> str:
        """ Returns the account max instances limit. (default is 1000) """
        try:
            response = client.describe_account_attributes(
                AttributeNames=['max-instances']
            )

            new_response = response['AccountAttributes'] \
            [0]['AttributeValues'][0]['AttributeValue']

            return new_response
        except ClientError as error:
            RequestExpired(error)


    @staticmethod
    def spotRequestsDescriber(client) -> set:
        """
        Dynamically retrieves all spot requests in a started | stopped
        state. (Will need to add the cancelled state in the future as
        it counts towards the limit)
        Returns the following:

        - index_list
        - types_list
        - inst_set
        """
        types_list = []
        inst_set = set()
        try:
            response = client.describe_spot_instance_requests(
                Filters=[
                    {
                        'Name': 'state',
                        'Values': ['active', 'open', 'closed']
                    }
                ]
            )

            for request in response['SpotInstanceRequests']:
                instance_types = request['LaunchSpecification']['InstanceType']

                # Creates a list of all the types.
                types_list.append(request['LaunchSpecification']['InstanceType'])

                # Sets indexes to choose from.
                inst_set.add(instance_types)
                index_list = list(inst_set)

            return (index_list, types_list, inst_set)
        except ClientError as error:
            RequestExpired(error)

    @staticmethod
    def ec2Describer(client):
        """
        Dynamically retrieves all instances in a started | stopped
        state. An index_list and types_list is returned for data
        manipulation outside the function.
        """
        inst_set = set()
        types_list = []

        try:
            response = client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name', 'Values': [
                            'running', 'stopped']
                    }
                ]
            )

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    types_list.append(str(instance['InstanceType']))

                inst_set.add(instance['InstanceType'])
                index_list = list(inst_set)

            return(index_list, types_list)
        except ClientError as error:
            RequestExpired(error)


    @staticmethod
    def volume_describer(client):
        volume_types = ['gp2', 'io1', 'st1', 'sc1', 'standard']
        try:
            response = client.describe_volumes(
                Filters=[
                    {
                        'Name': 'volume-type', 'Values': ['gp2']
                    },
                ],
            )
        except ClientError as error:
            print(error)

        pp_json(response)


    def limit_executor(self):
        """
        Triggers the appropiate functions depending on what service is
        used.

        Services supported:
        - OnDemand
        - SpotRequests
        - ReservedInstances - Future Implementation. Not Yet Set Up!
        """
        if self.service == 'OnDemand':
            print('{START}\r\n{text:^80}\r\n{END}'.format(
                text='~~ On Demand Instances ~~',
                START=Color.YELLOW,
                END=Color.END
                ))

            result = self.ec2Describer(self.client)

            if result != None:
                index_list, types_list = [result[0], result[1]]

                for type_name in index_list:
                    print('* On Demand Instance Type: {TYPE}, Currently '
                          'In Use: {ACTIVE}'.format(
                              TYPE=type_name,
                              ACTIVE=types_list.count(type_name)
                              )
                         )
                def_max = self.describe_max_inst(self.client)
                calc_percentage = percentage(len(types_list), def_max)

                print('\r\n* {PERCENTAGE}% Used by "On Demand" instances'
                      ' in this Region,  Current On Demand Instance Total: '
                      ' {USED},  Max On Demand Instances: {MAX} '
                      '{STATUS}'.format(
                          PERCENTAGE=calc_percentage,
                          USED=len(types_list),
                          MAX=def_max,
                          STATUS=status(calc_percentage),
                          )
                     )

        elif self.service == 'SpotRequests':
            print('{START}\r\n{TEXT:^80}\r\n{END}'.format(
                TEXT='~~ Spot Instance Requests ~~',
                START=Color.YELLOW,
                END=Color.END
                ))

            result = self.spotRequestsDescriber(self.client)

            if result != None:
                index_list, types_list, inst_set = [
                    result[0],
                    result[1],
                    result[2],
                    ]

                try:
                    for i in index_list:
                        print('* Spot Instance Type: {0}, Currently In an '
                              'Active | Open | Closed State: {1}'.format(
                                  i,
                                  types_list.count(i)
                                  )
                             )

                    total_count = len(types_list)
                    print('\r\n* Total Active Spot instances in this Region: '
                          '{0}'.format(total_count))
                except UnboundLocalError:
                    print('\r\n* Total Active Spot instances in this Region: '
                          '{0} {1}'.format('0', status('0')))

        elif self.service == 'EBS':
            print('{START}\r\n{TEXT:^80}\r\n{END}'.format(
                TEXT='~~ EBS Volumes ~~',
                START=Color.YELLOW,
                END=Color.END
                ))
            self.volume_describer(self.client)
