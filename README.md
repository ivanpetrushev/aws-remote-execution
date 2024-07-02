# aws-remote-execution

The goal of this demo is to show how to use AWS SQS to execute code on remote machine (EC2 or local).

## Prerequisites

- IAM user with permissions to sqs:SendMessage, sqs:DeleteMessage, sqs:ReceiveMessage
- 2 SQS queues configured - *trigger* and *output*, check the example in `test/sqs.tf` if unsure how to configure
- set queue URLs in `run-on-ec2.py`, `trigger-execution.py` and `retrieve-output.py`
- set command to execute in `run-on-ec2.py`
- `boto3` installed on target environment 

If you want to create test infrastructure:

- docker
- copy `test/.env.example` to `test/.env` and set your AWS credentials

## Structure

- `run-on-ec2.py` - script to run on the target machine (EC2 or even local) - it will listen for SQS messages, execute command and return output to a different queue
- `trigger-execution.py` - script to trigger execution - can be run locally, from Lambda, or can be ignored at all - SQS `sendMessage()` is what triggers the actual execution
- `retrieve-output.py` - script to retrieve output from the execution - can be run locally, from Lambda, or can be ignored at all - SQS `receiveMessage()` is what retrieves the output

- `test/` - Terraform configuration to quickly create SQS queues for testing, see below for details

## How to create test infrastructure

You need to apply Terraform in the `test/` directory.

```bash
cd test
make test-setup
```

This will create 2 SQS queues and output the queue URLs, which you can use to set in the scripts.

To destroy the test setup, you can run:

```bash
cd test
make test-destroy
```

## How to run

Copy `run-on-ec2.py` on the target machine. If it is an EC2 instance, make sure the instance has permissions to access the SQS queues.
Run the script on the target machine:
  
```bash
python3 run-on-ec2.py
```

This will run the script in the foreground. If you want to run it in the background, you can use `nohup`:

```bash
nohup python3 run-on-ec2.py &
```

To run the script at system boot, consult your OS documentation.

To trigger the execution, you can run `trigger-execution.py`:

```bash
python3 trigger-execution.py
```

To retrieve the output, you can run `retrieve-output.py`:

```bash
python3 retrieve-output.py
```

Output will be a JSON with 4 fields:

- `command` - command that was executed
- `stdout` - standard output of the command
- `stderr` - error output of the command, if any
- `timestamp` - timestamp of the execution

## TODO

Some improvement points:

- trigger message can be more complex, with more parameters like command parameters, timeout, host to run on
- SQS alarms to be raised when output is ready (for long running commands)
- SQS output to be send in a more convenient way (CloudWatch Logs, e-mail, Slack, etc.)
- SystemManager to be used to run commands instead of SQS
