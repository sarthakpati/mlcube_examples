FROM pytorch:1.9.0-cuda10.2-cudnn7-runtime
MAINTAINER MLPerf MLBox Working Group

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    python3-dev \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa -y && apt-get update

RUN apt-get install python3 -y

RUN apt-get install -y --no-install-recommends \ 
    python3.6 \
    python3.6-venv \
    python3.6-dev \
    python3-setuptools \
    wget \
    zip \
    unzip

RUN apt-get install python3-pip -y

RUN wget https://fets.projects.nitrc.org/FeTS_0.0.7_Installer.bin && chmod +x ./FeTS_*_Installer.bin

RUN yes | ./FeTS_${version}_Installer.bin --target ./fets_installation

RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./fets_installation/squashfs-root/usr/lib

RUN export PATH=$PATH:./fets_installation/squashfs-root/usr/bin

ENV LANG C.UTF-8

WORKDIR ./fets_installation/squashfs-root/usr/bin

ENTRYPOINT ["python3", "mlcube.py"]