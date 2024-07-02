import json
import os
import time
import boto3
import subprocess

SQS_TRIGGER = "https://sqs.eu-central-1.amazonaws.com/533267426035/re-demo-execution-trigger"
SQS_OUTPUT = "https://sqs.eu-central-1.amazonaws.com/533267426035/re-demo-execution-output"
CMD_TO_EXECUTE = "sleep 15; echo 'Hello, World!' > execution.log; echo 'Execution complete!'"

# Create an SQS client
sqs = boto3.client('sqs')

# poll for messages forever
while True:
    response = sqs.receive_message(
        QueueUrl=SQS_TRIGGER,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=20
    )
    if 'Messages' not in response:
        print('No messages in queue.')
        continue

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    print('Received message: %s' % message['Body'])
    print('Deleting message...')
    sqs.delete_message(
        QueueUrl=SQS_TRIGGER,
        ReceiptHandle=receipt_handle
    )
    # execute command, capture output
    print('Executing command...')
    result = subprocess.run(
        CMD_TO_EXECUTE, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    # compose new SQS message
    message = {
        'command': CMD_TO_EXECUTE,
        'stdout': stdout,
        'stderr': stderr,
        'timestamp': time.time()
    }
    # send message to SQS_OUTPUT
    response = sqs.send_message(
        QueueUrl=SQS_OUTPUT,
        MessageBody=json.dumps(message, ensure_ascii=False)
    )
    print('Sent message to output queue.')
