from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as api,
    core
)


class WorkshopPythonStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        queue = sqs.Queue(
            self, "WorkshopPythonQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "WorkshopPythonTopic"
        )

        bucket = s3.Bucket(self, id='s3cdkbucket',
                           bucket_name='udemycdkbucket123', versioned=True)

        lambdafunction = _lambda.Function(self, id='lambdafunction', runtime=_lambda.Runtime.PYTHON_3_7,
                                          handler='hello.handler', code=_lambda.Code.from_asset(path='lambdacode'))

        lambdaapi = api.LambdaRestApi(
            self, id="restapi", handler=lambdafunction)

        topic.add_subscription(subs.SqsSubscription(queue))
