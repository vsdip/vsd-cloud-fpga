FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1) Base dependencies (enough to build/run, use git, python, make, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    python3 \
    python3-dev \
    python-is-python3 \
    ca-certificates \
    libftdi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Optional: make "python" point to python3 (redundant with python-is-python3 but harmless)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /opt

# 2) OSS CAD Suite (Yosys, nextpnr-ice40, icestorm, etc.)
RUN set -eux; \
  curl -L "https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2025-10-31/oss-cad-suite-linux-x64-20251031.tgz" \
    -o /tmp/oss-cad.tgz; \
  mkdir -p /opt && tar -xzf /tmp/oss-cad.tgz -C /opt; \
  ln -s /opt/oss-cad-suite /opt/oss-cad; \
  rm /tmp/oss-cad.tgz

# 3) Put OSS CAD Suite tools first on PATH
ENV PATH="/opt/oss-cad/bin:${PATH}"

# Default workdir for your project (Codespace will mount repo here)
WORKDIR /workspace
