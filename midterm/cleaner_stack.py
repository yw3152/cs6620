from aws_cdk import Stack, aws_lambda as _lambda, aws_events as events, aws_events_targets as targets, Duration
from constructs import Construct

class CleanerStack(Stack):
    def __init__(self, scope: Construct, id: str, storage_stack, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Define the Cleaner Lambda function
        self.cleaner_lambda = _lambda.Function(
            self, "CleanerLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="cleaner.handler",
            code=_lambda.Code.from_asset("midterm/lambdas"),
            environment={
                "TABLE_NAME": storage_stack.table_t.table_name,
                "DEST_BUCKET": storage_stack.bucket_dst.bucket_name,
            }
        )

        # Grant permissions to the Cleaner Lambda
        storage_stack.bucket_dst.grant_delete(self.cleaner_lambda)
        storage_stack.table_t.grant_full_access(self.cleaner_lambda)

        # Create a CloudWatch Event rule to trigger Cleaner Lambda every 5 seconds
        rule = events.Rule(
            self, "CleanerSchedule",
            schedule=events.Schedule.rate(Duration.minutes(1))
        )
        rule.add_target(targets.LambdaFunction(self.cleaner_lambda))
