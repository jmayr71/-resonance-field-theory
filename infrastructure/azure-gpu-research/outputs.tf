output "resource_group_name" {
  description = "Created resource group."
  value       = azurerm_resource_group.rg.name
}

output "vm_name" {
  description = "GPU VM name."
  value       = azurerm_linux_virtual_machine.gpu.name
}

output "public_ip_address" {
  description = "Public IP address for SSH."
  value       = azurerm_public_ip.pip.ip_address
}

output "ssh_command" {
  description = "SSH command."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}

output "repo_dir" {
  description = "Repository directory on the VM."
  value       = var.repo_dir
}

output "runs_dir" {
  description = "Run output directory on the VM."
  value       = "/mnt/rft-data/runs"
}
