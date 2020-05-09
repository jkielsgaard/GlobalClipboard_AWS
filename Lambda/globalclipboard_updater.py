import boto3
import os

print('Loading function')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):

    bucket_name = os.environ['BUCKET_NAME'] 
    bucket_key = os.environ['BUCKET_KEY'] 
    lambda_function = os.environ['LAMBDA_FUNCTION']

    print('Updating GlobalClipboard backend lambda function')
    response = lambda_client.update_function_code(
        FunctionName=lambda_function,
        S3Bucket=bucket_name,
        S3Key=bucket_key
    )
    print(response)
