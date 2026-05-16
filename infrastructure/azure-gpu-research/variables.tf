variable "project" {
  description = "Project prefix used for Azure resource names."
  type        = string
  default     = "rft"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "research"
}

variable "location" {
  description = "Azure region. Use a region where the selected GPU SKU is available and quota is approved."
  type        = string
  default     = "westeurope"
}

variable "admin_username" {
  description = "Linux admin username."
  type        = string
  default     = "rftadmin"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key used for VM login."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to access SSH. Set this to your public IP /32. Do not leave 0.0.0.0/0 for real use."
  type        = string
}

variable "vm_size" {
  description = "Azure GPU VM size. Recommended phase-1 options depend on quota/region: NC A100, NC H100, L40S-capable NC-series, or ND A100."
  type        = string
  default     = "Standard_NC24ads_A100_v4"
}

variable "os_disk_size_gb" {
  description = "OS disk size in GB."
  type        = number
  default     = 256
}

variable "data_disk_size_gb" {
  description = "Data disk size in GB for runs, checkpoints, and artifacts."
  type        = number
  default     = 512
}

variable "data_disk_lun" {
  description = "LUN for the attached data disk."
  type        = number
  default     = 0
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

variable "shutdown_time" {
  description = "Daily auto-shutdown time in HHMM, local to timezone. Example: 2300."
  type        = string
  default     = "2300"
}

variable "shutdown_timezone" {
  description = "Timezone for auto-shutdown."
  type        = string
  default     = "W. Europe Standard Time"
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
