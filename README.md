# W251 Final Project

### To run the style transfer 
##### Building the docker file

On the jetson. 
```
sudo docker build DockerJetson -t neural_style 
xhost + 
```

##### Running for the jupyter notebook

```
docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --privileged --volume=/data:/data --name neural_style --device /dev/video1 -p 8888:8888  -d neural_style 
```

##### Running the style transfer script directly
Make sure that the neural\_style\_transfer directory is under /data/

```
docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --privileged --volume=/data:/data --name neural_style --device /dev/video1 -p 8888:8888 -it neural_style bash
cd /data/neural-style-transfer/
python3 neural_style_transfer_video.py --models=models/
```

Then be patient, its slow right now! Press Q to exit, N to switch to next model. 



### To train a new style transfer 
##### Building the docker file

On a cloud vm //TODO: need to test this out on a cloud vm
```
sudo docker build DockerCloud -t neural_style 
docker run -it --volume=/tmp:/tmp --volume=/data:/data --gpus all neural_style bash

th train.lua \
  -h5_file /data/ms-coco-256.h5 \
  -style_image FightingTemeraire.jpg \
  -style_image_size 384 \
  -content_weights 1.0 \
  -style_weights 5.0 \
  -checkpoint_name checkpoint \
  -gpu 0
```
