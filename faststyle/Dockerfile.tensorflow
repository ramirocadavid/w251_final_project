FROM datamachines/cuda_tensorflow_opencv:10.0_1.15.0_4.1.2-20191108

# Tagged build: docker build --tag="cudnn_tensorflow_opencv:10.0_1.13.2_4.1.2-20191108" .
# Tag version kept in sync with the datamachines/cuda_tensorflow_opencv one it is "FROM"

RUN mkdir /tmp/cudnn
COPY *.deb /tmp/cudnn/
RUN dpkg -i /tmp/cudnn/*.deb && rm -rf /tmp/cudnn 
