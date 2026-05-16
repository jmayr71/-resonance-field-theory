locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner_tag
    CostCenter  = var.cost_center_tag
    Workload    = "gpu-research"
    ManagedBy   = "terraform"
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${local.name_prefix}-${var.location}"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-${local.name_prefix}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.42.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "subnet" {
  name                 = "snet-gpu"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.42.1.0/24"]
}

resource "azurerm_public_ip" "pip" {
  name                = "pip-${local.name_prefix}-gpu01"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = local.common_tags
}

resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-${local.name_prefix}-gpu"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.common_tags

  security_rule {
    name                       = "AllowSSHFromAdminIP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.allowed_ssh_cidr
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "DenyInboundInternet"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface" "nic" {
  name                = "nic-${local.name_prefix}-gpu01"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.common_tags

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip.id
  }
}

resource "azurerm_network_interface_security_group_association" "nic_nsg" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

resource "azurerm_linux_virtual_machine" "gpu" {
  name                = "vm-${local.name_prefix}-gpu01"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.vm_size
  admin_username      = var.admin_username
  tags                = local.common_tags

  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.ssh_public_key_path)
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = var.os_disk_size_gb
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  custom_data = base64encode(templatefile("${path.module}/cloud-init.yaml", {
    admin_username = var.admin_username
    repo_url       = var.repo_url
    repo_dir       = var.repo_dir
    data_disk_lun  = var.data_disk_lun
  }))

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_managed_disk" "data" {
  name                 = "disk-${local.name_prefix}-gpu01-data"
  location             = azurerm_resource_group.rg.location
  resource_group_name  = azurerm_resource_group.rg.name
  storage_account_type = "Premium_LRS"
  create_option        = "Empty"
  disk_size_gb         = var.data_disk_size_gb
  tags                 = local.common_tags
}

resource "azurerm_virtual_machine_data_disk_attachment" "data" {
  managed_disk_id    = azurerm_managed_disk.data.id
  virtual_machine_id = azurerm_linux_virtual_machine.gpu.id
  lun                = var.data_disk_lun
  caching            = "ReadWrite"
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "shutdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.gpu.id
  location           = azurerm_resource_group.rg.location
  enabled            = true

  daily_recurrence_time = var.shutdown_time
  timezone              = var.shutdown_timezone

  notification_settings {
    enabled = false
  }

  tags = local.common_tags
}
