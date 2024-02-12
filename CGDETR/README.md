# CG-DETR을 이용한 Prediction

### Important
> Need to install `git-lfs` to download the model weights.

> After installing git-lfs, you need to `cd` to the path specified below and run `git-lfs pull` (It's all written below).

## Run-on-Vessl

### Install Git-LFS
```sh
apt update
apt install git-lfs
```

### Clone the repository
```sh
git clone [REPO_URL]
```

### Git-LFS Pull (This is for downloading the model weights)
```sh
cd CGDETR/run_on_video/CLIP_ckpt/qvhighlights_onlyCLIP
git-lfs pull
```

### Install miniconda3
```sh
cd CGDETR

mkdir -p ~/miniconda3

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

rm -rf ~/miniconda3/miniconda.sh

~/miniconda3/bin/conda init bash

reset # or restart your terminal
```

### Create conda environment (**must be** python 3.7)
```sh
conda create -n cgdetr python=3.7
conda activate cgdetr
```

###Install requirements
```sh
./install.sh
```

### Run the code
```sh
python main.py
```