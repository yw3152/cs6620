import boto3
import os
import time

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table_name = os.environ['TABLE_NAME']
destination_bucket = os.environ['DEST_BUCKET']
table = dynamodb.Table(table_name)

def handler(event, context):
    current_time = int(time.time())
    disown_threshold = 10  # seconds

    # Query DynamoDB for disowned objects
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('status').eq('DISOWNED')
    )
    
    for item in response['Items']:
        disown_timestamp = item['disown_timestamp']
        
        # Check if disowned object has exceeded the 10s threshold
        if current_time - disown_timestamp > disown_threshold:
            # Delete the copy from the destination bucket
            s3.delete_object(Bucket=destination_bucket, Key=item['copy_object_key'])
            
            # Delete the entry from DynamoDB
            table.delete_item(
                Key={
                    'original_object_name': item['original_object_name'],
                    'copy_timestamp': item['copy_timestamp']
                }
            )
