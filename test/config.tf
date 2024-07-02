terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.45.0"
    }
    random = {
      source = "hashicorp/random"
      version = "3.6.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  # region = "eu-west-1"
  default_tags {
    tags = {
      project = "${var.service}"
      workspace = terraform.workspace
    }
  }
}
