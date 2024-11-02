import aws_cdk as cdk
from aws_cdk import Stack, aws_dynamodb as dynamodb, aws_s3 as s3
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Define DynamoDB Table T
        self.table_t = dynamodb.Table(
            self, "TableT",
            partition_key=dynamodb.Attribute(name="original_object_name", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="copy_timestamp", type=dynamodb.AttributeType.NUMBER),
            time_to_live_attribute="disown_timestamp",
            removal_policy=cdk.RemovalPolicy.DESTROY  # Optional: Auto-deletes with stack
        )

        # Define S3 Buckets
        self.bucket_src = s3.Bucket(self, "BucketSrc")
        self.bucket_dst = s3.Bucket(self, "BucketDst")
