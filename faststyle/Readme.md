# Training using a new style image


### Setup folder

Download the folder into folder w251_final_project (after creating the folder). This folder consists of 
 - Dockerfile
 - Files required for training

Download the vgg16_weights.npz from google drive (link in email) to /faststyle/libs folder
Download libcudnn7_7.6.5.32-1+cuda10.0_amd.deb from https://drive.google.com/open?id=1oeMPx-ddyFL4QRMLCD2FzxJC1Atuq_yB to faststyle folder

The dockerfile will create a docker image with:
  - Python3
  - Tensorflow
  - Opencv
  - Cuda packages

### Build docker image

```sh
$cd faststyle/
$ docker build -t tensorflow .

```

### Run Docker Container

```sh
$docker run -it --name style_transfer --volume /root:/root -p 8800:8888 -d tensorflow
$docker attach style_transfer
$cd /root/w251_final_project/faststyle
```
### Download Data for Training

```sh
$apt install unzip
$unzip train2014.zip
```

### Convert image fines to Tensorflow files

```sh
$mkdir train2014_tf
$python3 tfrecords_writer.py --train_directory '/root/w251_final_project/faststyle/train2014' --output_directory '/root/w251_final_project/faststyle/train2014_tf' --train_shards 126 --num_threads 6
```

### Load new image to train a style

> Copy the new style image to style_images folder

### Training a model

```sh 
$python3 train.py --train_dir ./train2014_tf --style_img_path ./style_images/<nameofimage> --model_name <modelname> --n_epochs 2 --batch_size 32 --content_weights 0.5 --style_weights 5.0 5.0 5.0 5.0 --style_target_resize 0.5
```
