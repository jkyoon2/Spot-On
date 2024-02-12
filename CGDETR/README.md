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
cd /root

mkdir -p ~/miniconda3

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

rm -rf ~/miniconda3/miniconda.sh

~/miniconda3/bin/conda init bash

# Restart the ssh session after running the above command
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


### CG-DETR Input, Output format
Input:
```python
youtube_url = 'https://youtu.be/QTqvR6vVyfc?si=38hl4xafh7KWRbZX'
results_dict = run_example(youtube_url, 'A woman is walking on the street.')
```
Output:
```python
{
    'query': 'A woman is walking on the street.',
    'topk_moments': [130, 136, 138, 132, 140],
    'pred_scores': [-14.5234, -14.2812, -14.5859, ...] # 73
}

# Currently, images of topk_moments will be saved in the `examples` directory.
```