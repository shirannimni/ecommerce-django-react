terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.0"
    }
  }
}

variable "aws_config_file" {
  default = "~/.aws/config"
}

variable "aws_credentials_file" {
  default = "~/.aws/credentials"
}

provider "aws" {
  shared_config_files      = [var.aws_config_file]
  shared_credentials_files = [var.aws_credentials_file]
  profile                  = "default"
  region                   = "eu-west-2"
}

resource "aws_ebs_volume" "jenkins_volume" {
  availability_zone = "eu-west-2a"
  size              = 15
}

data "aws_vpc" "default" {
  default = true
}


data "aws_security_group" "jenkins_master" {
  filter {
    name   = "group-id"
    values = ["sg-0e6a24325ecdf3ee4"]
  }
}

data "aws_security_group" "my_ubuntu" {
  filter {
    name   = "group-id"
    values = ["sg-07cec9c4da763f9f7"]
  }
}

data "aws_security_group" "my_windows" {
  filter {
    name   = "group-id"
    values = ["sg-069098eafc8f563ec"]
  }
}



resource "aws_instance" "jenkins" {
  ami               = "ami-09627c82937ccdd6d"
  instance_type     = "t3.micro"
  #security_groups   = [data.aws_security_group.jenkins_master.id]
  availability_zone = "eu-west-2a"
  key_name          = "shiran-tlv"

  vpc_security_group_ids = [
    data.aws_security_group.jenkins_master.id,
    data.aws_security_group.my_ubuntu.id,
    data.aws_security_group.my_windows.id,
  ]

  root_block_device {
    volume_size          = 15
    delete_on_termination = true
  }

  depends_on = [
    data.aws_security_group.jenkins_master,
    data.aws_security_group.my_ubuntu,
    data.aws_security_group.my_windows
  ]
  
  tags = {
    Name = "jenkins_master"
  }

  user_data = <<-EOF
   #!/bin/bash

   service_name="jenkins"

   # Update package index
   sudo apt-get update

   # Install Java
   sudo apt-get install -y openjdk-17-jdk

   # Install Jenkins
   sudo apt update
   sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
   https://pkg.jenkins.io/debian/jenkins.io-2023.key
   echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
   https://pkg.jenkins.io/debian binary/ | sudo tee \
   /etc/apt/sources.list.d/jenkins.list > /dev/null
   sudo apt-get update
   sudo apt-get install jenkins
   
   # Start Jenkins
   sudo systemctl start jenkins
   sudo systemctl enable jenkins

   # Install Git
   sudo apt-get install -y git

   # Install Docker
   sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-  properties-common
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io

   # Configure Firewall
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw allow 8080/tcp
   sudo ufw allow 22/tcp
   sudo ufw allow 5000
   sudo ufw enable
   EOF
}

resource "aws_volume_attachment" "jenkins_va" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.jenkins_volume.id
  instance_id = aws_instance.jenkins.id
}

resource "aws_instance" "my_ubuntu" {
  ami               = "ami-09627c82937ccdd6d"    
  instance_type     = "t3.micro"
  availability_zone = "eu-west-2a"
  key_name          = "shiran-tlv"

  vpc_security_group_ids = [
    data.aws_security_group.jenkins_master.id,
    data.aws_security_group.my_ubuntu.id,
    data.aws_security_group.my_windows.id,
  ]

  root_block_device {
    volume_size          = 8
    delete_on_termination = true
  }

  tags = {
    Name = "my_ubuntu"
  }

  user_data = <<-EOF
    #!/bin/bash
    # Update the system
    sudo apt update

    # Install Git
    sudo apt-get install -y git

    # Install Docker
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker

    # Configure Firewall
    sudo ufw allow 80
    sudo ufw allow 443
    sudo ufw allow 8080/tcp
    sudo ufw allow 5000
    sudo ufw allow 22/tcp
    sudo ufw enable
    EOF
}

resource "aws_ebs_volume" "ubuntu_volume" {
  availability_zone = "eu-west-2a"
  size              = 8
}

resource "aws_volume_attachment" "ubuntu_va" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.ubuntu_volume.id
  instance_id = aws_instance.my_ubuntu.id
}

resource "aws_instance" "my_windows" {
  ami               = "ami-0b2ff60c5f576d8ee"
  instance_type     = "t3.micro"
  availability_zone = "eu-west-2a"
  key_name          = "shiran-windows"

  vpc_security_group_ids = [
    data.aws_security_group.jenkins_master.id,
    data.aws_security_group.my_ubuntu.id,
    data.aws_security_group.my_windows.id,
  ]

  root_block_device {
    volume_size          = 30
    delete_on_termination = true
  }

  tags = {
    Name = "my_windows"
  }

  user_data = <<-EOF
    <powershell>
    Start-Transcript -Path "C:\install.log"
    Install-PackageProvider -name NuGet -MinimumVersion 2.8.5.201 -Force
    Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
    Install-Module -Name PowerShellGet -Force -AllowClobber
    Install-Module -Name PackageManagement -Force -AllowClobber

    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

    $env:Path += ";$($env:ALLUSERSPROFILE)\chocolatey\bin"
    choco install git -y
    choco install docker-desktop -y

    ufw allow 8080/tcp  # Jenkins
    ufw allow 2376 # Docker API
    ufw allow 5901
    ufw allow 3389
    ufw allow 80
    ufw allow 443
    ufw allow 22/tcp
    ufw enable

    Stop-Transcript
    </powershell>
  EOF
}

resource "aws_ebs_volume" "windows_volume" {
  availability_zone = "eu-west-2a"
  size              = 30
}

resource "aws_volume_attachment" "windows_va" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.windows_volume.id
  instance_id = aws_instance.my_windows.id
}

