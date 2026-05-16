# Multicloud GPU Research Setup

## Strategy

The project uses a pragmatic multicloud model:

```text
Azure = primary provider
AWS   = secondary / burst provider
GCP   = later optional provider
Local NVIDIA / DGX / RunPod / Lambda = tactical execution targets
```

The goal is not to make every cloud identical. The goal is to make the scientific runtime portable:

```text
same repository
same container
same Python/CUDA/PyTorch versions
same run configuration format
same output structure
same diagnostics
```

Cloud-specific networking, IAM, disks and VM resources remain cloud-specific Terraform modules.

## Current Modules

```text
infrastructure/common/container
infrastructure/common/scripts
infrastructure/azure-gpu-research
infrastructure/aws-gpu-research
```

## Runtime Standard

The portable runtime is defined in:

```text
infrastructure/common/container/Dockerfile.cuda
```

It provides:

- PyTorch CUDA runtime,
- NumPy,
- SciPy,
- Pandas,
- Matplotlib,
- tqdm,
- PyYAML,
- Rich,
- GPU smoke test,
- shared entrypoint.

## Azure Module

Use Azure as the default target for controlled research runs.

Best suited for:

- primary baselines,
- reproducible long-running tests,
- medium/large convergence studies,
- integration with enterprise cloud governance.

Folder:

```text
infrastructure/azure-gpu-research
```

Typical starting SKU:

```text
Standard_NC24ads_A100_v4
```

Alternative larger SKU:

```text
Standard_ND96asr_v4
```

The exact SKU depends on region and quota.

## AWS Module

Use AWS as secondary capacity or for Spot/Burst execution.

Best suited for:

- GPU availability fallback,
- tactical parameter sweeps,
- cost/performance comparison,
- Spot-capable batch jobs.

Folder:

```text
infrastructure/aws-gpu-research
```

Typical low-entry development instance:

```text
g5.2xlarge
```

For larger production runs, use p4/p5-class instances only after quota and cost approval.

## GCP Module

Not implemented yet by design.

GCP becomes relevant if:

- JAX becomes a primary implementation path,
- GCP GPU quota/pricing is attractive,
- or TPU-based experiments become relevant.

Current project code is PyTorch/CUDA-oriented, so Azure/AWS are higher priority.

## What Must Stay Portable

The following must be cloud-neutral:

```text
src/
configs/
runs metadata
CSV/JSON/NPY outputs
container image
experiment runner CLI
```

The following does not need to be cloud-neutral:

```text
VNet/VPC
subnets
security groups
managed disks
IAM/roles
VM naming
shutdown scheduling
```

## Recommended Execution Pattern

1. Develop locally or on a small GPU target.
2. Validate in the common CUDA container.
3. Run medium tests on Azure.
4. Burst large or cheap sweeps to AWS when beneficial.
5. Store results in provider-local disk first.
6. Copy important artifacts back to GitHub releases, object storage, or local archive.

## Cost Controls

Always:

- restrict SSH to your public IP,
- stop/deallocate GPU VMs when idle,
- use daily shutdown on Azure,
- monitor EBS/managed disk persistence costs,
- use Spot only for checkpointable jobs,
- write run metadata with instance type, region, commit SHA and config.

## Next Engineering Steps

1. Refactor experiments into reusable `src/` modules.
2. Add a common runner CLI.
3. Add YAML configs for sweeps.
4. Add GPU device selection.
5. Add structured run metadata.
6. Add resume/checkpoint support.
7. Add optional object storage upload.

## Target Convergence Study

The first serious multicloud-compatible study should sweep:

```text
N = 64, 96, 128
L = 40, 60, 80
v = 0.0, 0.2, 0.4, 0.6
boundary = hard, soft
```

Primary diagnostics:

```text
Q
E/E0
E²-P²
sigma_x/sigma_x0
energy drift
constraint drift
boundary topological density
```
