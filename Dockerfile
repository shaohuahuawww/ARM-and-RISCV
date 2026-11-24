FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup && \
    apt-get update && apt-get install -y --no-install-recommends \
    make python3 curl ca-certificates xz-utils bzip2 \
    gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi \
    gcc-riscv64-unknown-elf binutils-riscv64-unknown-elf \
    qemu-system-arm iverilog \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
