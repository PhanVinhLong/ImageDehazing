import os,argparse
import numpy as np
from PIL import Image
import ntpath

import torch
import torch.nn as nn
import torchvision.transforms as tfs 
import torchvision.utils as vutils
import matplotlib.pyplot as plt
from torchvision.utils import make_grid

import sys
sys.path.insert(0, './FFANet/net')
from models import *

FFA_dir = os.getcwd()+'/FFANet/net/'

def tensorShow(tensors,titles=['haze']):
        fig=plt.figure()
        for tensor,tit,i in zip(tensors,titles,range(len(tensors))):
            img = make_grid(tensor)
            npimg = img.numpy()
            ax = fig.add_subplot(221+i)
            ax.imshow(np.transpose(npimg, (1, 2, 0)))
            ax.set_title(tit)
        plt.show()

gps=3
blocks=19

def TestFFA(img_dir, output_dir, dataset):
    print("img_path:",img_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    model_dir=FFA_dir+f'trained_models/{dataset}_train_ffa_{gps}_{blocks}.pk'
    device='cuda' if torch.cuda.is_available() else 'cpu'
    ckp=torch.load(model_dir,map_location=device)
    net=FFA(gps=gps,blocks=blocks)
    net=nn.DataParallel(net)
    net.load_state_dict(ckp['model'])
    net.eval()

    haze = Image.open(img_dir)
    haze1= tfs.Compose([
        tfs.ToTensor(),
        tfs.Normalize(mean=[0.64, 0.6, 0.58],std=[0.14,0.15, 0.152])
    ])(haze)[None,::]
    haze_no=tfs.ToTensor()(haze)[None,::]
    with torch.no_grad():
        pred = net(haze1)
    ts=torch.squeeze(pred.clamp(0,1).cpu())
    img_fname=ntpath.basename(img_dir)
    _, img_ext = os.path.splitext(img_fname)
    pred_path=output_dir+img_fname.split('.')[0]+'_FFA'+img_ext
    vutils.save_image(ts, pred_path)
    return pred_path