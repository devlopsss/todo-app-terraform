terraform {
  backend "s3" {
    bucket  = "todo-app-terraform-state-642494479460"
    key     = "todo-app/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}
