resource "aws_sqs_queue" "trigger" {
  name = "${var.service}-execution-trigger"
  delay_seconds = 0
  max_message_size = 262144
  message_retention_seconds = 3600 * 24 * 14
  receive_wait_time_seconds = 0 # short polling vs long polling
  visibility_timeout_seconds = 30
}

resource "aws_sqs_queue" "output" {
  name = "${var.service}-execution-output"
  delay_seconds = 0
  max_message_size = 262144
  message_retention_seconds = 3600 * 24 * 14
  receive_wait_time_seconds = 0 # short polling vs long polling
  visibility_timeout_seconds = 30
}

output "queue_url_trigger" {
  value = aws_sqs_queue.trigger.id
}

output "queue_url_output" {
  value = aws_sqs_queue.output.id
}