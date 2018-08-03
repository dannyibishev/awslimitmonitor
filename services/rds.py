from botocore.exceptions import ClientError, NoRegionError
from functionality.tools import Color, pp_json, status, percentage
from networking.connections import RequestExpired

class RDSManager:
    """
    Houses all of the methods and attributes which are required to
    calculate and return all RDS Related limits.
    """
    def __init__(self, service, client) -> str:
        """
        this class will need to be initialised with the correct service
        before using any other method/function within the class.
        """
        self.service = service
        self.client = client

    @staticmethod
    def rdsDescriber(client) -> dict:
        dictReturner = {}
        count = 0
        try:
            response = client.describe_account_attributes()['AccountQuotas']
            for quota in response:
                calc_percentage = percentage(quota['Used'], quota['Max'])
                quota['percentage'] = calc_percentage
                dictReturner['RDSLimit.' + str(count)] = quota
                count += 1

            return dictReturner

        except ClientError as e:
            print(e)

    def limit_executor(self):
        """
        Triggers the appropiate functions depending on what service is
        used.

        Services supported:
        - RelationalDatabasesService
        """

        if self.service == 'RelationalDatabasesService':
            print('{START}\r\n{TEXT:^80}\r\n{END}'.format(
                TEXT = '~~ Important RDS Limits ~~',
                START = Color.YELLOW,
                END = Color.END
                ))
            limitdict = self.rdsDescriber(self.client)

            if limitdict:
                for limit in limitdict.values():
                    print('* {PERCENTAGE}% Used for the RDS Limit: '
                          '{LIMIT}, Used: {USED}, Max: {MAX} {STATUS}'.format(
                              PERCENTAGE = limit['percentage'],
                              LIMIT = limit['AccountQuotaName'],
                              USED = limit['Used'],
                              MAX = limit['Max'],
                              STATUS = status(limit['percentage']),
                              )
                          )
