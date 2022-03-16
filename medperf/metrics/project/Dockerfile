FROM cbica/captk:release-1.8.1

RUN yum install -y xz-devel

RUN pip install --upgrade pip

RUN pip install pandas synapseclient nibabel

COPY Hausdorff95 /work/CaPTk/bin/.

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa -y && apt-get update

RUN apt-get install python3.8 python3-pip -y

COPY ./requirements.txt project/requirements.txt 

RUN pip3 install --upgrade pip

RUN pip3 install --default-timeout=10000 --no-cache-dir -r project/requirements.txt

ENV LANG C.UTF-8

COPY . /project

WORKDIR /project

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "mlcube.py"]