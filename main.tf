terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

module "cognito" {
  source   = "./modules/cognito"
  app_name = var.app_name
}

module "dynamodb" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}

module "secrets_manager" {
  source                = "./modules/secrets_manager"
  app_name              = var.app_name
  cognito_client_id     = module.cognito.client_id
  cognito_client_secret = module.cognito.client_secret
}

module "iam" {
  source       = "./modules/iam"
  app_name     = var.app_name
  dynamodb_arn = module.dynamodb.table_arn
  cognito_arn  = module.cognito.user_pool_arn
  secret_arn   = module.secrets_manager.secret_arn
}

module "lambda" {
  source          = "./modules/lambda"
  app_name        = var.app_name
  lambda_role_arn = module.iam.lambda_role_arn
  secret_name     = module.secrets_manager.secret_name
  dynamodb_table  = module.dynamodb.table_name
}

module "api_gateway" {
  source      = "./modules/api_gateway"
  app_name    = var.app_name
  lambda_arns = module.lambda.function_arns
  account_id  = var.account_id
  aws_region  = var.aws_region
}

module "s3" {
  source   = "./modules/s3"
  app_name = var.app_name
}
