FROM python:3.9
LABEL maintainer="Ivan Iziumov <i.izyumov@marketlab.pl>"

RUN apt-get update -y && apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev libatlas-base-dev libhdf5-dev

RUN mkdir arm_prosthetic
WORKDIR /arm_prosthetic 

COPY requirements.txt /arm_prosthetic/requirements.txt
COPY ./rpi_zero_soft_arm/ /arm_prosthetic/rpi_zero_soft_arm/
COPY ./common/ /arm_prosthetic/common/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install https://releases.linaro.org/components/ldcg/tensorflow-aarch64/r2.7.0/h5py/h5py-3.1.0-cp39-cp39-linux_aarch64.whl
RUN python3 -m pip install -r /arm_prosthetic/requirements.txt
