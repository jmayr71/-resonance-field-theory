variable "project" {
  description = "Project prefix used for AWS resource names."
  type        = string
  default     = "rft"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "research"
}

variable "aws_region" {
  description = "AWS region. Choose a region where the selected GPU instance type is available and quota-approved."
  type        = string
  default     = "eu-central-1"
}

variable "availability_zone" {
  description = "Optional explicit availability zone. Leave empty for provider default subnet AZ selection."
  type        = string
  default     = ""
}

variable "admin_username" {
  description = "Linux admin username. Ubuntu AMIs normally use ubuntu."
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key used for EC2 login."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to access SSH. Set this to your public IP /32."
  type        = string
}

variable "instance_type" {
  description = "AWS GPU instance type. Examples: g5.xlarge, g5.2xlarge, g6.xlarge, p4d.24xlarge, p5.48xlarge. Select based on quota and cost."
  type        = string
  default     = "g5.2xlarge"
}

variable "root_volume_size_gb" {
  description = "Root EBS volume size in GB."
  type        = number
  default     = 256
}

variable "data_volume_size_gb" {
  description = "Data EBS volume size in GB for runs and artifacts."
  type        = number
  default     = 512
}

variable "repo_url" {
  description = "Git repository URL to clone on the VM."
  type        = string
  default     = "https://github.com/jmayr71/-resonance-field-theory.git"
}

variable "repo_dir" {
  description = "Directory where the repository will be cloned."
  type        = string
  default     = "/opt/rft/-resonance-field-theory"
}

variable "owner_tag" {
  description = "Owner/contact tag."
  type        = string
  default     = "johannes"
}

variable "cost_center_tag" {
  description = "Cost center tag."
  type        = string
  default     = "research"
}
