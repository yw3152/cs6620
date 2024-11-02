from aws_cdk import Stack, aws_lambda as _lambda
from constructs import Construct

class ReplicatorStack(Stack):
    def __init__(self, scope: Construct, id: str, storage_stack, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Define the Replicator Lambda function
        self.replicator_lambda = _lambda.Function(
            self, "ReplicatorLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="replicator.handler",
            code=_lambda.Code.from_asset("midterm/lambdas"),
            environment={
                "TABLE_NAME": storage_stack.table_t.table_name,
                "DEST_BUCKET": storage_stack.bucket_dst.bucket_name,
            }
        )

        # Grant permissions to the Replicator Lambda
        storage_stack.bucket_src.grant_read(self.replicator_lambda)
        storage_stack.bucket_dst.grant_write(self.replicator_lambda)
        storage_stack.table_t.grant_full_access(self.replicator_lambda)
