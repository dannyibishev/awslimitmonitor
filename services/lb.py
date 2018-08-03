from botocore.exceptions import ClientError, NoRegionError
from functionality.tools import Color, pp_json, status, percentage
from networking.connections import RequestExpired

class LBManager:
    """
    Houses all of the methods and attributes which are required to
    calculate and return the limits for the loab balancer servuce.
    """
    def __init__(self, service, albclient, elbclient) -> str:
        """
        this class will need to be initialised with the correct service
        before using any other method/function within the class.
        """
        self.service = service
        self.albclient = albclient
        self.elbclient = elbclient


    def lbmaster(funct):
        print('TESTING {0}'.format(funct))
        def albRetriever(client):
            """Function used to calculate total ALB's."""
            try:
                response = albclient.describe_load_balancers()
                base_count_alb = 0
                for alb_list in response['LoadBalancers']:
                    base_count_alb += 1

                return base_count_alb
            except ClientError as e:
                print(e)

        def elbRetriever(elbclient):
            """Function is used to calculate total ELB's."""
            try:
                response = elbclient.describe_load_balancers()
                base_count_elb = 0
                for alb_list in response['LoadBalancerDescriptions']:
                    base_count_elb += 1

                return base_count_elb
            except ClientError as e:
                print(e)


    @lbmaster
    def lbDescriber(client):
        """
        Use the calculations from the describe_loab_balancer functions,
        which in turn is calculated against the max to get the percentage.
        """
        try:
            limit_output = client.describe_account_limits()
            # pp_json(response)
            # limit_output = (response.values())

            pp_json(limit_output)
            # lb_max = int(limit_output[1][0]['Max'])
            # alb_output = str(float('%.0f' % describe_load_balancers_alb()) / lb_max * 100).split('.')[0]
            # elb_output = str(float('%.0f' % describe_load_balancers_elb()) / lb_max * 100).split('.')[0]


        except ClientError as e:
            print(e)

    def limit_executor(self):
        """
        Triggers the appropiate functions depending on what service is
        used.

        Services supported:
        - LoadBalancer
        - TargetGroup
        """

        if self.service == 'LoadBalancer':
            print('{START}\r\n{text:^80}\r\n{END}'.format(
                text='~~ ALB, ELB AND NLB Limits ~~',
                START=Color.YELLOW,
                END=Color.END
                ))

            self.lbDescriber(self.albclient)
            self.lbDescriber(self.elbclient)

        if self.service == 'TargetGroup':
            print('{START}\r\n{text:^80}\r\n{END}'.format(
                text='~~ Target Groups ~~',
                START=Color.YELLOW,
                END=Color.END
                ))


        # client = boto3.client('elb')
        # response = client.describe_account_limits()
        # pp_json(response)

        # sendinput = str(int(alb_output[:2]))
        # print(sendinput + "% Used for ALBs, Current ALB count: " + str(describe_load_balancers_alb()) + "  Max ALB: " + str(lb_max) + errors(sendinput))
        # sendinput = str(int(elb_output[:2]))
        # print(sendinput + "% Used for ELBs, Current ELB count: " + str(describe_load_balancers_elb()) + "  Max ELB: " + str(lb_max) + errors(sendinput))
