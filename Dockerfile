# Dockerfile

FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
build-essential \
    cmake \
    cppcheck \
    valgrind \
    clang \
    clang-tidy \
    python3 \
    python3-pip \
    git \
    nano \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

CMD ["/bin/bash"]