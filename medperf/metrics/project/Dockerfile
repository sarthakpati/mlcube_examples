FROM cbica/captk:release-1.8.1

RUN yum install -y xz-devel

RUN pip install --upgrade pip

RUN pip install pandas synapseclient nibabel

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa -y && apt-get update

RUN apt-get install python3.8 python3-pip -y

RUN cd /work/CaPTk/bin/ && \
    wget https://captk.projects.nitrc.org/Hausdorff95_linux.zip && \
    unzip Hausdorff95_linux.zip && \
    rm Hausdorff95_linux.zip

COPY ./requirements.txt project/requirements.txt 

RUN pip3 install --upgrade pip

RUN pip3 install --default-timeout=10000 --no-cache-dir -r project/requirements.txt

ENV LANG C.UTF-8

COPY . /project

WORKDIR /project

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "mlcube.py"]