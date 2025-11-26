FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    python3 python3-pip \
    make \
    pkg-config \
    cmake \
    clang \
    g++ \
    libffi-dev \
    libreadline-dev \
    bison flex \
    libboost-all-dev \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Install yosys, nextpnr-ice40, icestorm ---
# Option A: use distro packages (simpler, maybe older versions)
RUN apt-get update && apt-get install -y \
    yosys \
    nextpnr-ice40 \
    icestorm \
    && rm -rf /var/lib/apt/lists/*

# Set Python alias
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /workspace

