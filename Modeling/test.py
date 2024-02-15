import pickle
import torch
from text_search import TextSearchModel

pickle_path = "./dataset/item_list_emb.pickle"
image_dir = "./segmentation_images"
device = "cpu"
client_id = "7mjrb3lKMrT9UIGQwmSB"
client_secret = "5O9ezGkzdy"

model = TextSearchModel(pickle_path, image_dir, device, client_id, client_secret)
list = model.search("black shirt")

print(list)