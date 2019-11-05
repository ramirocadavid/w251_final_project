FROM w251/pytorch:dev-tx2-4.2.1_b97

# To run use below
#docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --privileged --volume=/data:/data --volume=/tmp:/tmp --network hw03 --name neural_style --device /dev/video1 -p 8888:8888  -d neural_style


RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

#ARG URL=http://169.44.201.108:7002/jetpacks/4.2.1

WORKDIR /tmp

RUN cd ~ && git clone https://github.com/opencv/opencv.git && \
    cd opencv && \
    mkdir -p build && cd build && \
    cmake .. && make && \
    make install

RUN pip3 install imutils


RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 


RUN mkdir /data

WORKDIR /data

RUN wget -N http://images.cocodataset.org/zips/train2017.zip && \
    wget -N http://images.cocodataset.org/zips/val2017.zip 
    
RUN apt install unzip && \
    unzip train2017.zip && \
    unzip val2017.zip

RUN git clone https://github.com/jcjohnson/fast-neural-style.git && \
    cd fast-neural-style && \
    sed -i 's/curl/wget/g' models/download_style_transfer_models.sh && \
    sed -i 's/-O/-N/g' models/download_style_transfer_models.sh && \
    sed -i 's/curl/wget/g' models/download_vgg16.sh && \
    sed -i 's/-O/-N/g' models/download_vgg16.sh 

RUN apt-get -y install libc-dev
RUN apt-get -y install build-essential
RUN apt-get -y install python-h5py    
RUN pip3 install Pillow==3.3.1 && \
    pip3 install six==1.10.0

RUN pip3 install --upgrade pip
#RUN pip3 install scipy
    

RUN pip3 install imutils

RUN pip3 install jupyter

ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y python3-sklearn

WORKDIR /
RUN mkdir -p notebooks
WORKDIR /notebooks

EXPOSE 8888

# Jupyter
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root


