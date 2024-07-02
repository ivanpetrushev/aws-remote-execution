include .env
export $(shell sed 's/=.*//' .env)

TF_IMAGE = hashicorp/terraform:1.8.1
TERRAFORM_CMD = docker run -i -t -v ${PWD}:/work -w /work --env-file .env ${TF_IMAGE}

init:
	${TERRAFORM_CMD} init

apply-test:
	${TERRAFORM_CMD} apply

destroy-test:
	${TERRAFORM_CMD} destroy

test-setup: init apply-test