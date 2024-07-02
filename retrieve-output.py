import boto3

SQS_OUTPUT = "https://sqs.eu-central-1.amazonaws.com/533267426035/re-demo-execution-output"

# Create an SQS client
sqs = boto3.client('sqs')

# poll for messages forever
while True:
    response = sqs.receive_message(
        QueueUrl=SQS_OUTPUT,
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
    print('Received message: %s' % response['Messages'][0]['Body'])
    print('Deleting message...')
    receipt_handle = response['Messages'][0]['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=SQS_OUTPUT,
        ReceiptHandle=receipt_handle
    )
