import os
import torch
import pickle
from typing import List
from transformers import CLIPModel, CLIPProcessor

class TextSearchModel():
    def __init__(self, pickle_path: str, image_dir: str, device):
        self.num_images = 1000

        # TODO 1: Initialize CLIP text model
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # TODO 2: Load encoded image features (pickle file)
        with open(pickle_path, "rb") as file:
            self.pickle = pickle.load(file)

        # TODO 3: Initialize image file path list ('./images/000000.jpg', ...)
        self.image_file_path_list = [os.path.join(image_dir, image) for image in os.listdir(image_dir)]

        # TODO 4: Initialize Papago API client
        self.papago = None

        # TODO 5: Initialize hyperparameter of weights for each similarity score
        self.weights = None

    def encode_text(self, query_text: str) -> torch.Tensor:
        # TODO 1: Encode the query_text using CLIP text model
        text_token = self.processor(query_text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            text_embed = self.model.get_text_features(**text_token)
        return text_embed
    
    def calculate_text_similarity(self, query_text_emb: torch.Tensor) -> List[float]:
        # TODO 4: Calculate similarity scores between the query_text and,
        # 1. All big category names (only 1 for each image)
        # 2. All small category names (only 1 for each image)
        # 3. All image hashtags (>= 0 hashtags in the image, may vary per image)
        
        # TODO 5: Calculate the overall similarity score for each image
        # 1. query text vs big category names: List[float], length = num_images
        # 2. query text vs small category names: List[float], length = num_images
        # 3. query text vs image hashtags: List[float], length = num_images
        #  - The number of hashtags may vary per image, but the length of the list
        #  should be the same as the number of images (num_images)
        return [0.0] * self.num_images

    def calculate_image_similarity(self, query_text_emb: torch.Tensor) -> List[float]:
        # TODO 6: Calculate similarity scores between the query_text and image features
        return [0.0] * self.num_images
    

    def search(self, query_text: str, top_k: int = 3) -> List[str]:
        similarity_scores = self.calculate_similarity(query_text)
        # TODO 6: Sort the image file path list based on the similarity scores
        # TODO 7: Return the top 3 image file paths
        return ['000000.jpg', '000001.jpg', '000002.jpg']
    
