import os
import json
import torch
import pickle
import requests
import numpy as np

from typing import List
from transformers import CLIPModel, CLIPProcessor
from sklearn.metrics.pairwise import cosine_similarity

class TextSearchModel:
    def __init__(self, pickle_path: str, image_dir: str, device, client_id, client_secret,url='https://openapi.naver.com/v1/papago/n2mt'):
        self.num_images = 1000
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.device = device

        # TODO 1: Initialize CLIP text model
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # TODO 2: Load encoded image features (pickle file)
        with open(pickle_path, "rb") as file:
            self.pickle = pickle.load(file)

        # TODO 3: Initialize image file path list ('./images/000000.jpg', ...)
        self.image_file_path_list = [os.path.join(image_dir, image) for image in os.listdir(image_dir)]

        # TODO 5: Initialize hyperparameter of weights for each similarity score
        self.w_big = 1
        self.w_small = 1
        self.w_image = 1

    def translate(self, query_text: str) -> str:
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        data = {
            "source": "ko",
            "target": "en",
            "text": query_text
        }
        response = requests.post(self.url, headers=headers, data=data)
        result = json.loads(response.text)
        return result['message']['result']['translatedText']

    def encode_text(self, query_text: str) -> torch.Tensor:
        # TODO 1: Encode the query_text using CLIP text model

        query_text = self.translate(query_text)
        text_token = self.processor(query_text, return_tensors="pt", padding=True, truncation=True).to(self.device)

        with torch.no_grad():
            text_embed = self.model.get_text_features(**text_token)
        return text_embed
    
    def calculate_text_similarity(self, query_text_emb: torch.Tensor) -> List[float]:

        query_text_emb = query_text_emb.reshape(1,-1)

        tensor_list = [self.pickle[key]["big_category_embed"] for key in sorted(self.pickle.keys())]
        big_category_emb_mat = torch.cat(tensor_list, dim=0)

        tensor_list = [self.pickle[key]["small_category_embed"] for key in sorted(self.pickle.keys())]
        small_category_emb_mat = torch.cat(tensor_list, dim=0)

        query_text_emb = query_text_emb.detach().cpu().numpy()

        big_category_emb_mat = big_category_emb_mat.cpu().numpy()
        big_similarity_score = cosine_similarity(big_category_emb_mat, query_text_emb)

        small_category_emb_mat = small_category_emb_mat.cpu().numpy()
        small_similarity_score = cosine_similarity(small_category_emb_mat, query_text_emb)

        return [big_similarity_score, small_similarity_score]

    def calculate_image_similarity(self, query_text_emb: torch.Tensor) -> List[float]:

        query_text_emb = query_text_emb.reshape(1,-1)
        
        tensor_list = [self.pickle[key]["image_embed"] for key in sorted(self.pickle.keys())]
        image_emb_mat = torch.cat(tensor_list, dim=0)

        image_emb_mat = image_emb_mat.cpu().numpy()
        query_text_emb = query_text_emb.detach().cpu().numpy()
        image_similarity_score = cosine_similarity(image_emb_mat, query_text_emb)

        return image_similarity_score
    

    def search(self, query_text: str, top_k: int = 5) -> List[str]:
        query_text_emb = self.encode_text(query_text)
        big_score, small_score = self.calculate_text_similarity(query_text_emb)
        image_score = self.calculate_image_similarity(query_text_emb)
        
        weighted_sum = big_score * self.w_big + small_score * self.w_small + image_score * self.w_image
        
        sorted_indices = np.argsort(weighted_sum, axis=0)
        sorted_items = np.array(self.image_file_path_list)[sorted_indices]
        return sorted_items[:5]
