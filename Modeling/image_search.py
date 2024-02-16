import torch
import requests
import json
from typing import List
from transformers import CLIPModel, CLIPProcessor
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import numpy as np

import logging
import pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageSearchModel:
    def __init__(self, pickle_path: str, image_dir: str, device, client_id, client_secret,url='https://openapi.naver.com/v1/papago/n2mt'):
        self.num_images = 1000
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.device = device

        # Initialize CLIP model
        logger.info("Loading CLIP text model...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Load pickle file
        logger.info("Loading encoded image features...")
        with open(pickle_path, "rb") as file:
            self.pickle = pickle.load(file)
        
        # Initialize image file path list ('./images/000000.jpg', ...)
        self.image_file_path_list = [f"images/{key}.jpg" for key in sorted(self.pickle.keys())]

        # TODO 5: Initialize hyperparameter of weights for each similarity score
        self.w_big = 1
        self.w_small = 1
        self.w_image = 3

        # TODO 1: Initialize CLIP text model
        # TODO 2: Initialize CLIP image model
        # TODO 3: Initialize image segmentation model
        # TODO 4: Load encoded image features (pickle file)
        # TODO 5: Load encoded text features (pickle file)
        # TODO 6: Initialize Papago API client
        # TODO 7: Initialize hyperparameter of weights for each similarity score

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
        logger.info(f"Translated query text: {query_text}")

        text_token = self.processor(query_text, return_tensors="pt", padding=True, truncation=True).to(self.device)

        with torch.no_grad():
            text_embed = self.model.get_text_features(**text_token)
        return text_embed
    
    def segment_image(self, image_file_path: str, query_text: str, save_path: str) -> str:
        # TODO 1: Segment the image using the image segmentation model
        # This should be done using inter process communication (IPC)
        # Use socket, pipe, or any other method to communicate with the image segmentation model
        # TODO 2: Save the segmented image to the disk

        return './static/segmented_images/000000.jpg'
    
    def encode_image(self, image_path) -> torch.Tensor:
        # TODO 2: Encode the image using CLIP image model
        image = Image.open(image_path)
        image_token = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_embed = self.model.get_image_features(**image_token)
        return image_embed

    
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

    def calculate_image_similarity(self, query_image_emb: torch.Tensor) -> List[float]:
        # TODO 6: Calculate similarity scores between the query_image and image features
        tensor_list = [self.pickle[key]["image_embed"] for key in sorted(self.pickle.keys())]
        image_emb_mat = torch.cat(tensor_list, dim=0).cpu().numpy()
        query_image_emb = query_image_emb.reshape(1,-1).detach().cpu().numpy()
        image_similarity_score = cosine_similarity(image_emb_mat, query_image_emb)

        return image_similarity_score

    def search(self, query_image_path, query_text: str, top_k: int = 5) -> List[str]:
        # TODO 1: Segment and save the query_image using the image segmentation model
        # TODO 2: Encode the query_image and query_text using CLIP models
        query_image_emb = self.encode_image(query_image_path)
        query_text_emb = self.encode_text(query_text)

        big_score, small_score = self.calculate_text_similarity(query_text_emb)
        image_score = self.calculate_image_similarity(query_image_emb)

        weighted_sum = big_score * self.w_big + small_score * self.w_small + image_score * self.w_image
        sorted_indices = weighted_sum.argsort(axis=0)[::-1]
        sorted_items = np.array(self.image_file_path_list)[sorted_indices]

        return sorted_items[:top_k].flatten().tolist()
