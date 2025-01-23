provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_instance" "example" {
  ami           = "ami-097c5c21a18dc59ea"
  instance_type = "t3.micro"
  
  tags = {
    Name = "Jenkins-Terraform-EPA"
  }
}

