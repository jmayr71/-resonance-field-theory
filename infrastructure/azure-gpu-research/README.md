# Azure GPU Research Environment

## Purpose

This folder contains the initial Azure infrastructure configuration for running larger GPU-backed simulations for the resonance field theory / covariant baby-Skyrme programme.

The setup is intentionally pragmatic:

- one Linux GPU VM,
- restricted SSH access,
- attached data disk,
- Python/PyTorch bootstrap,
- repository checkout,
- daily auto-shutdown to reduce cost.

It is intended for phase-1 numerical scaling, not for a managed enterprise HPC platform.

## Target Use Cases

Use this environment for:

- higher-resolution covariant solver tests,
- larger-domain rest-soliton relaxation,
- Lorentz convergence studies,
- boost parameter sweeps,
- boundary-condition experiments,
- longer multi-soliton runs.

## Recommended VM Size

Start with a single-GPU A100/L40S/H100-capable VM if available in your Azure region and subscription quota.

Suggested starting point:

```text
Standard_NC24ads_A100_v4
```

Alternative larger class:

```text
Standard_ND96asr_v4
```

The exact SKU must be confirmed in the Azure Portal because availability and quota vary by subscription and region.

## Files

```text
providers.tf              Terraform provider configuration
variables.tf              Input variables
main.tf                   Azure resources
outputs.tf                Useful outputs after deployment
cloud-init.yaml           VM bootstrap script
terraform.tfvars.example  Example variable file
```

## Azure Resources Created

The Terraform configuration creates:

- Resource Group
- Virtual Network
- Subnet
- Network Security Group
- Public IP
- Network Interface
- Ubuntu 22.04 Linux GPU VM
- Managed data disk
- Data disk attachment
- Daily auto-shutdown schedule

## Security Defaults

SSH is restricted by:

```text
allowed_ssh_cidr
```

Set this to your public IP with `/32`. Do not use `0.0.0.0/0` for real use.

Password login is disabled. SSH key authentication is required.

## Cost Control

The setup includes daily auto-shutdown:

```text
shutdown_time = "2300"
shutdown_timezone = "W. Europe Standard Time"
```

This is important because GPU VMs are expensive even when idle.

Additional recommendations:

1. Deallocate the VM when not in use.
2. Use Azure budgets and cost alerts.
3. Consider Spot VMs only for checkpointed batch workloads.
4. Keep the data disk persistent, but stop compute when not needed.

## Prerequisites

Install locally:

```bash
az --version
terraform version
ssh -V
```

Login:

```bash
az login
az account set --subscription "<subscription-id>"
```

Check your public IP:

```bash
curl ifconfig.me
```

Create SSH key if needed:

```bash
ssh-keygen -t ed25519 -C "rft-azure" -f ~/.ssh/rft_azure_ed25519
```

Then set:

```text
ssh_public_key_path = "~/.ssh/rft_azure_ed25519.pub"
```

## Deployment

Copy the example variable file:

```bash
cd infrastructure/azure-gpu-research
cp terraform.tfvars.example terraform.tfvars
```

Edit:

```bash
nano terraform.tfvars
```

At minimum set:

```text
allowed_ssh_cidr = "<your-public-ip>/32"
ssh_public_key_path = "~/.ssh/<your-key>.pub"
vm_size = "<quota-approved-gpu-sku>"
location = "<region-with-gpu-quota>"
```

Initialize and deploy:

```bash
terraform init
terraform plan
terraform apply
```

After deployment, Terraform outputs an SSH command.

## First Login

SSH to the VM:

```bash
ssh rftadmin@<public-ip>
```

Then run:

```bash
source /opt/rft/activate.sh
nvidia-smi
python /opt/rft/gpu_smoke_test.py
```

The repository is located at:

```text
/opt/rft/-resonance-field-theory
```

Run outputs should go to:

```text
/mnt/rft-data/runs
/mnt/rft-data/artifacts
```

## Troubleshooting

Check cloud-init:

```bash
sudo tail -n 200 /var/log/cloud-init-output.log
sudo tail -n 200 /var/log/rft-bootstrap.log
```

Check GPU:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If CUDA is unavailable, install or update the NVIDIA driver extension or use an Azure GPU image with drivers preinstalled.

## Destroy Environment

To delete all resources:

```bash
terraform destroy
```

If you want to preserve run data, copy it out of `/mnt/rft-data` before destroying.

## Next Engineering Steps

After the VM is available, the repository should be refactored into reusable GPU-capable modules:

```text
src/models
src/solvers
src/diagnostics
configs
runs
```

Then we can run systematic convergence studies:

```text
N = 64, 96, 128, 256
L = 40, 60, 80
v = 0.0, 0.2, 0.4, 0.6
boundary = hard, soft
```

Primary metrics:

```text
Q
E/E0
E²-P²
sigma_x/sigma_x0
energy drift
constraint drift
boundary topological density
```
