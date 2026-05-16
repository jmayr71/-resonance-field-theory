output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.gpu.id
}

output "public_ip" {
  description = "EC2 public IP address."
  value       = aws_instance.gpu.public_ip
}

output "ssh_command" {
  description = "SSH command."
  value       = "ssh ${var.admin_username}@${aws_instance.gpu.public_ip}"
}

output "repo_dir" {
  description = "Repository directory on the EC2 instance."
  value       = var.repo_dir
}

output "runs_dir" {
  description = "Run output directory on the EC2 instance."
  value       = "/mnt/rft-data/runs"
}
