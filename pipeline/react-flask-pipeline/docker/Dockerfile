FROM tensorflow/tensorflow:1.15.0-gpu-py3
ENV DEBIAN_FRONTEND=noninteractive

# Install linux utilities
RUN apt-get update
RUN apt-get -y install wget
RUN apt-get -y install zip
RUN apt-get -y install vim
RUN apt install -y python-opencv
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt -y update && apt -y install yarn

# Install python libraries
RUN apt-get update
RUN pip3 install --user flask
RUN pip3 install --user flask-cors 
RUN pip3 install --user scikit-image
RUN pip3 install --user Pillow
RUN pip3 install --user opencv-python
RUN pip3 install --user gdown
