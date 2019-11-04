FROM w251/pytorch:dev-tx2-4.2.1_b97

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
WORKDIR /tmp
RUN cd ~ && git clone https://github.com/opencv/opencv.git && \
   cd opencv && \
   mkdir -p build && cd build && \
   cmake .. && make && \
   make install
RUN pip3 install imutils
RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
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

