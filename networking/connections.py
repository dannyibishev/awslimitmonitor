import sys

class RequestExpired:
    def __init__(self, ClientErrorException):
        if "RequestExpired" in str(ClientErrorException):
            print('An error occurred: RequestExpired. This has most likely occured due to an expired sts token.')
        else:
            print(ClientErrorException)
            sys.exit()
