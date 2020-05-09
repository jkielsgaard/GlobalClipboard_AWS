import boto3
import os
import json

print('Loading Lambda function')
s3 = boto3.resource('s3')


bucket_name = os.environ['BUCKET_NAME'] 


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def respondhtml(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': res,
        'headers': {
            'Content-Type': 'text/html',
        },
    }

def blockexist(block):
    bucket = s3.Bucket(bucket_name)
    objs = map(lambda x: (x.key), bucket.objects.all())

    if block in objs:
        return True
    else:
        return False

def readBlock(block_key):
    obj = s3.Object(bucket_name, block_key)
    blockdata = obj.get()['Body'].read().decode('utf-8')
    return blockdata

def writeBlock(block_key, data):
    obj = s3.Object(bucket_name, block_key)
    obj.put(Body=data)
    
def deletBlockdata(block_key):
    obj = s3.Object(bucket_name, block_key)
    obj.put(Body='')


def lambda_handler(event, context):

    httpMethod = event['httpMethod']

   
    if httpMethod == 'POST':
        function = event['queryStringParameters']['function']
        block = event['queryStringParameters']['block']
        if blockexist(block):
            if function == 'copy':
                data = event['body']
                writeBlock(block, data)
                res = 'copy'
            elif function == 'paste':
                res = readBlock(block)
            elif function == 'delete':
                deletBlockdata(block)
                res = 'deleted'
            elif function == 'public':
                data = event['body']
                writeBlock('PUBLICBLOCK', data)
                res = 'public copy'
            return respond(None, res)
        else:
            if function == 'copy':
                data = event['body']
                writeBlock(block, data)
                return respond(None, 'copy')
            else:
                return respond('Block doesnt exist')
    elif httpMethod == 'GET':
        block = 'PUBLICBLOCK'
        if blockexist(block):
            res = readBlock('PUBLICBLOCK')
            return respondhtml(None, res)
        else:
            return respond('Block doesnt exist')
    else:
        return respond('Unsupported method')