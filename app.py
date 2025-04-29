#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


app = cdk.App()
env_EU = cdk.Environment(account="439964561764", region="us-east-1")
CdkWorkshopStack(app, "CdkWorkshopStack",env=env_EU)

app.synth()
