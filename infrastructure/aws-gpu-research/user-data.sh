#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${repo_url}"
REPO_DIR="${repo_dir}"
DATA_DIR="/mnt/rft-data"
RUNS_DIR="$DATA_DIR/runs"
ARTIFACTS_DIR="$DATA_DIR/artifacts"

exec > >(tee /var/log/rft-bootstrap.log | logger -t rft-bootstrap -s 2>/dev/console) 2>&1

echo "[RFT] Starting AWS GPU bootstrap"
apt-get update
apt-get install -y git curl wget unzip build-essential python3-venv python3-pip python3-dev htop tmux jq ca-certificates

mkdir -p "$DATA_DIR"

# Format and mount attached EBS data volume if present.
# On Nitro instances, /dev/sdf often appears as /dev/nvme1n1.
DATA_DEVICE=""
for dev in /dev/nvme1n1 /dev/xvdf /dev/sdf; do
  if [ -b "$dev" ]; then
    DATA_DEVICE="$dev"
    break
  fi
done

if [ -n "$DATA_DEVICE" ]; then
  if ! blkid "$DATA_DEVICE"; then
    mkfs.ext4 -F "$DATA_DEVICE"
  fi
  if ! grep -q "$DATA_DIR" /etc/fstab; then
    echo "$DATA_DEVICE $DATA_DIR ext4 defaults,nofail 0 2" >> /etc/fstab
  fi
  mount -a
fi

mkdir -p /opt/rft "$RUNS_DIR" "$ARTIFACTS_DIR"
chown -R ubuntu:ubuntu /opt/rft "$DATA_DIR" || true

# Install Docker and NVIDIA Container Toolkit.
curl -fsSL https://raw.githubusercontent.com/jmayr71/-resonance-field-theory/main/infrastructure/common/scripts/install-nvidia-docker-ubuntu.sh -o /opt/rft/install-nvidia-docker-ubuntu.sh
chmod +x /opt/rft/install-nvidia-docker-ubuntu.sh
sudo -u ubuntu bash /opt/rft/install-nvidia-docker-ubuntu.sh || bash /opt/rft/install-nvidia-docker-ubuntu.sh

# Clone repo.
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone "$REPO_URL" "$REPO_DIR"
else
  cd "$REPO_DIR"
  git pull --ff-only || true
fi
chown -R ubuntu:ubuntu "$REPO_DIR"

# Build portable runtime image.
cd "$REPO_DIR/infrastructure/common/container"
docker build -t rft-cuda:latest .

cat >/opt/rft/run-container.sh <<'EOS'
#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="/opt/rft/-resonance-field-theory"
DATA_DIR="/mnt/rft-data"
docker run --rm -it --gpus all \
  -v "$REPO_DIR":/workspace/-resonance-field-theory \
  -v "$DATA_DIR/runs":/runs \
  -v "$DATA_DIR/artifacts":/artifacts \
  -e RFT_REPO=/workspace/-resonance-field-theory \
  -e RFT_RUNS=/runs \
  -e RFT_ARTIFACTS=/artifacts \
  rft-cuda:latest "$@"
EOS
chmod +x /opt/rft/run-container.sh
chown ubuntu:ubuntu /opt/rft/run-container.sh

cat >/opt/rft/README_NEXT_STEPS.txt <<'EOS'
RFT AWS GPU VM setup
====================

After SSH login:

  nvidia-smi
  /opt/rft/run-container.sh python /opt/rft/gpu_smoke_test.py

Repository:

  /opt/rft/-resonance-field-theory

Data:

  /mnt/rft-data/runs
  /mnt/rft-data/artifacts

Run an interactive container:

  /opt/rft/run-container.sh bash

Cost control:

  Stop EC2 when not in use.
  EBS data volume remains persistent and continues to cost money.
EOS

echo "[RFT] AWS GPU bootstrap complete"
