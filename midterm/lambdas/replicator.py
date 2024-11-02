import boto3
import os
import time

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table_name = os.environ['TABLE_NAME']
destination_bucket = os.environ['DEST_BUCKET']
table = dynamodb.Table(table_name)

def handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        if event_name.startswith("ObjectCreated:"):
            handle_put_event(source_bucket, object_key)
        elif event_name.startswith("ObjectRemoved:"):
            handle_delete_event(object_key)

def handle_put_event(source_bucket, object_key):
    timestamp = int(time.time())
    copy_key = f"{object_key}_copy_{timestamp}"
    
    # Copy the object to the destination bucket
    s3.copy_object(
        Bucket=destination_bucket,
        CopySource={'Bucket': source_bucket, 'Key': object_key},
        Key=copy_key
    )
    
    # Retrieve all copies of the original object from DynamoDB
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('original_object_name').eq(object_key)
    )
    
    copies = response['Items']
    
    # Delete the oldest copy if there are any existing copies
    if copies:
        oldest_copy = min(copies, key=lambda x: x['copy_timestamp'])
        s3.delete_object(Bucket=destination_bucket, Key=oldest_copy['copy_object_key'])
        table.delete_item(
            Key={
                'original_object_name': object_key,
                'copy_timestamp': oldest_copy['copy_timestamp']
            }
        )
    
    # Insert the new copy into DynamoDB
    table.put_item(
        Item={
            'original_object_name': object_key,
            'copy_timestamp': timestamp,
            'copy_object_key': copy_key,
            'status': 'ACTIVE',
            'disown_timestamp': None
        }
    )

def handle_delete_event(object_key):
    # Mark the object in DynamoDB as disowned
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('original_object_name').eq(object_key)
    )
    
    for item in response['Items']:
        table.update_item(
            Key={
                'original_object_name': object_key,
                'copy_timestamp': item['copy_timestamp']
            },
            UpdateExpression="SET #status = :disowned, disown_timestamp = :now",
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':disowned': 'DISOWNED',
                ':now': int(time.time())
            }
        )
