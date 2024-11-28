provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "platyfin" {
  name = "platyfin"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-0453ec754f44f9a4a" # Update this to a valid x86_64 AMI ID
  instance_type = "t3.micro"

  tags = {
    Name = "AppServer"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              amazon-linux-extras install postgresql14 -y
              service docker start
              service postgresql start
              usermod -a -G docker ec2-user
              sudo -u postgres psql -c "CREATE USER rinku WITH PASSWORD 'EatBig';"
              sudo -u postgres psql -c "CREATE DATABASE ushur;"
              sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ushur TO rinku;"
              docker run -d -p 5000:5000 --name platyfin ${aws_ecr_repository.platyfin.repository_url}:latest
              EOF
}

resource "aws_security_group" "app_sg" {
  name        = "app_sg"
  description = "Allow inbound traffic"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_route53_zone" "main" {
  name = "banjarajogi.com"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.banjarajogi.com"
  type    = "A"
  ttl     = "300"
  records = [aws_instance.app_server.public_ip]
}