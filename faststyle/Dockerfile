FROM w251/tensorflow:dev-tx2-4.2.1_b97

# This is a container for Keras and Jupyter
# docker run --name keras --privileged -p 8888:8888 -d w251/keras:dev-tx2-4.2.1_b97-py3 

ARG URL=http://169.44.201.108:7002/jetpacks/4.2

RUN apt-get update && apt install -y git pkg-config wget build-essential cmake unzip


WORKDIR /tmp
# RUN rm *.deb

RUN curl $URL/libopencv_3.3.1-2-g31ccdfe11_arm64.deb  -so libopencv_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb

RUN apt install -y  libtbb-dev libavcodec-dev libavformat-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev
RUN apt install -y libswscale-dev libv4l-dev
RUN dpkg -i *.deb



RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

RUN apt update
RUN apt install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    wget

RUN pip3 install jupyter
#RUN pip3 install pandas

ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3-sklearn
RUN pip3 install keras

WORKDIR /
RUN mkdir -p notebooks
WORKDIR /notebooks

RUN pip install paho-mqtt

RUN pip install pybase64

EXPOSE 8888

# Jupyter
#CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root
