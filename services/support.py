import boto3
import botocore.exceptions

client = boto3.client('support')

# response = client.describe_trusted_advisor_checks(
#     language='en'
# )

response = client.describe_services(
    serviceCodeList=[
        'string',
    ],
    language='en'
)

print(response)
