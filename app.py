#!/usr/bin/env python3
import os

import aws_cdk as cdk

from midterm.storage_stack import StorageStack
from midterm.replicator_stack import ReplicatorStack
from midterm.cleaner_stack import CleanerStack


app = cdk.App()
storage_stack = StorageStack(app, "StorageStack")
replicator_stack = ReplicatorStack(app, "ReplicatorStack", storage_stack=storage_stack)
cleaner_stack = CleanerStack(app, "CleanerStack", storage_stack=storage_stack)

app.synth()
