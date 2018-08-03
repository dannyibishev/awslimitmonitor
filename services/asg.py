"""
The ASG Module, awslimitmonitor imports this to calculate
all ASG limits.
"""

from botocore.exceptions import ClientError
from functionality.tools import Color, status, percentage


class ASGManager:
    """
    Houses all of the methods and attributes which are required to
    calculate and return the limits for ASG and Launch Configurations.
    """
    def __init__(self, service, client) -> str:
        """Initialise the service and client for use with methods."""
        self.service = service
        self.client = client


    @staticmethod
    def describe_account_limits_asg(client) -> dict:
        """
        Dynamically retrieves all asg and lc limits.

        - Returns a dictionary.
        """
        try:
            print('{START}\r\n{text:^80}\r\n{END}'.format(
                text='~~ Launch Config and ASG Limits ~~',
                START=Color.YELLOW,
                END=Color.END)
                 )

            response = client.describe_account_limits()

            max_asg = response['MaxNumberOfAutoScalingGroups']
            used_asg = response['NumberOfAutoScalingGroups']
            max_launch_configs = response['MaxNumberOfLaunchConfigurations']
            used_launch_configs = response['NumberOfLaunchConfigurations']

            calc_percentage_asg = percentage(
                used_asg,
                max_asg,
                )

            calc_percentage_lc = percentage(
                used_launch_configs,
                max_launch_configs
                )

            return {'MaxASG': max_asg,
                    'UsedASG': used_asg,
                    'UsedLC': used_launch_configs,
                    'MaxLC': max_launch_configs,
                    'LaunchConfigPercentage': calc_percentage_lc,
                    'ASGPercentage': calc_percentage_asg,
                   }
        except ClientError as error:
            print(error)


    def limit_executor(self):
        """
        Triggers the appropiate functions depending on what service is used.

        Services supported:
        - AutoScalingGoups
        """
        asg = self.describe_account_limits_asg(self.client)
        if asg:
            print('* {percentage}% Used for Launch Configs, Launch Config'
                  ' Used: {used}, Max Launch Configs: {max} {status}'.format(
                      percentage=asg['LaunchConfigPercentage'],
                      used=asg['UsedLC'],
                      max=asg['MaxLC'],
                      status=status(asg['LaunchConfigPercentage'],)
                      )
                 )

            print('* {percentage}% Used for Auto Scaling Groups, Launch Config'
                  ' Used: {used}, Max ASG: {max} {status}'.format(
                      percentage=asg['ASGPercentage'],
                      used=asg['UsedASG'],
                      max=asg['MaxASG'],
                      status=status(asg['ASGPercentage'],)
                      )
                 )
