#!/usr/bin/env bash
set -euo pipefail

mkdir -p "${RFT_RUNS:-/runs}" "${RFT_ARTIFACTS:-/artifacts}"

if [ -d "${RFT_REPO:-/workspace/-resonance-field-theory}" ]; then
  cd "${RFT_REPO:-/workspace/-resonance-field-theory}"
else
  cd /workspace
fi

exec "$@"
