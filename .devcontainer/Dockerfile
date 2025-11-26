FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1) Base dependencies
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    autotools-dev \
    build-essential \
    clang \
    bison \
    flex \
    libreadline-dev \
    gawk \
    tcl-dev \
    libffi-dev \
    cmake \
    curl \
    git \
    graphviz \
    xdot \
    pkg-config \
    python3 \
    python3-dev \
    python-is-python3 \
    mercurial \
    libboost-system-dev \
    libboost-python-dev \
    libboost-filesystem-dev \
    libboost-all-dev \
    libeigen3-dev \
    zlib1g-dev \
    libmpc-dev \
    libftdi-dev \
    libmpfr-dev \
    libgmp-dev \
    texinfo \
    gperf \
    libtool \
    patchutils \
    bc \
    libexpat-dev \
    qtbase5-dev \
    && rm -rf /var/lib/apt/lists/*

# (optional but harmless now; ensures `python` → python3)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /opt

# 2) Install IceStorm from source
RUN git clone https://github.com/YosysHQ/icestorm.git && \
    cd icestorm && \
    make -j"$(nproc)" && \
    make install && \
    cd .. && \
    rm -rf icestorm

# 3) Install nextpnr (ice40) from source
RUN git clone --recurse-submodules https://github.com/YosysHQ/nextpnr.git && \
    cd nextpnr && \
    mkdir build && cd build && \
    cmake .. -DARCH=ice40 && \
    make -j"$(nproc)" && \
    make install && \
    cd /opt && \
    rm -rf nextpnr

# 4) OSS CAD Suite (Yosys, etc.)
RUN set -eux; \
  curl -L "https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2025-10-31/oss-cad-suite-linux-x64-20251031.tgz" \
    -o /tmp/oss-cad.tgz; \
  mkdir -p /opt && tar -xzf /tmp/oss-cad.tgz -C /opt; \
  ln -s /opt/oss-cad-suite /opt/oss-cad; \
  rm /tmp/oss-cad.tgz

# 5) Put OSS CAD Suite tools first on PATH
ENV PATH="/opt/oss-cad/bin:${PATH}"

# Default workdir for your project (Codespace will mount repo here)
WORKDIR /workspace
