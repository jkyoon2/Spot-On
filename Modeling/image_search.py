import torch
from typing import List

class ImageSearchModel:
    def __init__(self):
        self.num_images = 1000
        # TODO 1: Initialize CLIP text model
        # TODO 2: Initialize CLIP image model
        # TODO 3: Initialize image segmentation model
        # TODO 4: Load encoded image features (pickle file)
        # TODO 5: Load encoded text features (pickle file)
        # TODO 6: Initialize Papago API client
        # TODO 7: Initialize hyperparameter of weights for each similarity score
    
    def segment_image(self, image_file_path: str, query_text: str, save_path: str) -> str:
        # TODO 1: Segment the image using the image segmentation model
        # TODO 2: Save the segmented image to the disk

        return './static/segmented_images/000000.jpg'
    
    def encode_image(self, image_file_path: str) -> torch.Tensor:
        # TODO 2: Encode the image using CLIP image model
        return torch.zeros(512)

    def encode_text(self, query_text: str) -> torch.Tensor:
        # TODO 1: Encode the query_text using CLIP text model
        return torch.zeros(512)
    
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

    def calculate_image_similarity(self, query_image_emb: torch.Tensor) -> List[float]:
        # TODO 6: Calculate similarity scores between the query_image and image features
        return [0.0] * self.num_images

    def search(self, query_image, query_text: str, top_k: int = 5) -> List[str]:
        # TODO 1: Segment and save the query_image using the image segmentation model
        # TODO 2: Encode the query_image and query_text using CLIP models
        # TODO 3: Calculate similarity scores between the query_text and text features
        # TODO 4: Calculate similarity scores between the query_image and image features
        # TODO 5: Calculate the overall similarity score for each image (with weights)
        # TODO 6: Sort the image file path list based on the similarity scores
        # TODO 7: Return the top 3 image file paths
        return ['000000.jpg', '000001.jpg', '000002.jpg', '000003.jpg', '000004.jpg']
