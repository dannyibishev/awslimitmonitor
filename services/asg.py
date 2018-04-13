import boto3
from botocore.exceptions import ClientError
from functionality.tools import Color, pp_json, status, percentage
from networking.connections import RequestExpired


class ASGManager:
    """
    Houses all of the methods and attributes which are required to calculate and return the limits for ASG and Launch Configurations.
    """
    def __init__(self, service) -> str:
        """ this class will need to be initialised with the correct service before using any other method/function within the class."""
        self.service = service

    @staticmethod
    def describe_account_limits_asg() -> dict:
        """
        Dynamically retrieves all asg and launch configuration limits in one api call.
        - Returns a dictionary.
        """

        client = boto3.client('autoscaling')
        try:
            print('{START}\r\n{text:^80}\r\n{END}'.format(text='~~ Launch Config and ASG Limits ~~', START=Color.YELLOW, END=Color.END))

            response = client.describe_account_limits()

            maxASG = response['MaxNumberOfAutoScalingGroups']
            usedASG = response['NumberOfAutoScalingGroups']
            maxLaunchConfigs = response['MaxNumberOfLaunchConfigurations']
            usedLaunchConfigs = response['NumberOfLaunchConfigurations']

            calcPercentageASG = percentage(usedASG,maxASG)
            calcPercentageLC = percentage(usedLaunchConfigs,maxLaunchConfigs)

            return {'MaxASG':maxASG, 'UsedASG':usedASG, 'UsedLC':usedLaunchConfigs, 'MaxLC':maxLaunchConfigs, 'LaunchConfigPercentage':calcPercentageLC, 'ASGPercentage':calcPercentageASG}

        except ClientError as e:
            print(e)

    def limitExecutor(self):
        """
        Triggers the appropiate functions depending on what service is used.

        Services supported:
        - AutoScalingGoups
        """
        asg = self.describe_account_limits_asg()

        if asg:
            print('* {percentage}% Used for Launch Configs, Launch Config Used: {used}, Max Launch Configs: {max} {status}'.format(indent=': 5',percentage=asg['LaunchConfigPercentage'],used=asg['UsedLC'],max=asg['MaxLC'],status=status(asg['LaunchConfigPercentage'])))
            print('* {percentage}% Used for Auto Scaling Groups, Launch Config Used: {used}, Max ASG: {max} {status}'.format(indent=': 5',percentage=asg['ASGPercentage'],used=asg['UsedASG'],max=asg['MaxASG'],status=status(asg['ASGPercentage'])))
