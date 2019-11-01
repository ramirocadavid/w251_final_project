FROM nightseas/cuda-torch

RUN apt-get update
RUN apt-get install -y libhdf5-dev


WORKDIR /data
RUN wget -N http://images.cocodataset.org/zips/train2017.zip
RUN wget -N http://images.cocodataset.org/zips/val2017.zip

RUN unzip train2017.zip
RUN unzip val2017.zip

RUN git clone https://github.com/jcjohnson/fast-neural-style.git

WORKDIR /data/fast-neural-style/

RUN sed -i 's/curl/wget/g' models/download_style_transfer_models.sh
RUN sed -i 's/-O/-N/g' models/download_style_transfer_models.sh
RUN sed -i 's/curl/wget/g' models/download_vgg16.sh
RUN sed -i 's/-O/-N/g' models/download_vgg16.sh

RUN bash models/download_style_transfer_models.sh
RUN bash models/download_vgg16.sh

RUN pip install -r requirements.txt

RUN python scripts/make_style_dataset.py \
  --train_dir /data/train2017/ \
  --val_dir /data/val2017/ \
  --output_file /data/ms-coco-256.h5

RUN luarocks install https://raw.githubusercontent.com/deepmind/torch-hdf5/master/hdf5-0-0.rockspec

