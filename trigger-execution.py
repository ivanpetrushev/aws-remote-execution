import boto3

SQS_TRIGGER = "https://sqs.eu-central-1.amazonaws.com/533267426035/re-demo-execution-trigger"

# Create an SQS client
sqs = boto3.client('sqs')

# Send message to SQS queue
# if more sophisticated approach is needed, MessageBody can become a JSON object with command to execute, host, parameters, etc...
response = sqs.send_message(
    QueueUrl=SQS_TRIGGER,
    MessageBody=(
        'Run the execution!' 
    )
)
