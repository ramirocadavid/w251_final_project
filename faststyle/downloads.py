import gdown
import wget
url = 'https://drive.google.com/uc?id='

def cuddn():
    id_cudnn = '1oeMPx-ddyFL4QRMLCD2FzxJC1Atuq_yB'
    output_cudnn = './libcudnn7_7.6.5.32-1+cuda10.0_amd.deb'
    print("Downloading CUDNN")
    gdown.download(url + id_cudnn, output_cudnn, quiet=False)

def vgg_16():
    id_vgg16 = '166FO7IKc-sWCjRCH7eoXde9lidgOxWG4'
    output_vgg16 = './libs/vgg16_weights.npz'
    print("Downloading VGG16 weights")
    gdown.download(url + id_vgg16, output_vgg16, quiet=False)
    
def coco():
    url_coco = 'http://images.cocodataset.org/zips/train2014.zip'
    output_coco = './train2014.zip'
    print("Downloading COCO dataset (13 GB)")
    wget.download(url_coco, output_coco)

if __name__ == "__main__":
    try:
        coco()
        vgg_16()
        cudnn()
    except:
        print("ERROR: Make sure you are located at faststyle/libs folder")
