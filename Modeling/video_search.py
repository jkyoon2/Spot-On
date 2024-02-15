import torch
from typing import List

class VideoSearchModel:
    def __init__(self):
        self.num_images = 1000
        # TODO 1: Initialize CG-DETR model
        # TODO 2: Initialize ImageSearchModel
    

    def search_moments(self, query_video: str, query_text: str, top_k: int = 5) -> str:
        # TODO 1: Translate the query_text to English using Papago API
        # TODO 2: Get top-k moments & scores from the CG-DETR model
        # TODO 3: Extract images of 10 frames & top-k momdents from the query_video
        # TODO 4: Visualize the scores (Movie CLIP and scores)

        results = {}
        results['visualization'] = 'visualization.jpg'
        results['selectedMoments'] = [
            {'image': "./static/000000.jpg"},
            {'image': "./static/000001.jpg"},
            {'image': "./static/000002.jpg"},
            {'image': "./static/000003.jpg"},
            {'image': "./static/000004.jpg"}
        ]

        return results

    def search_images(self, query_image, query_text: str, top_k: int = 5) -> List[str]:
        # TODO 1: Use the ImageSearchModel to search images

        return ['000000.jpg', '000001.jpg', '000002.jpg', '000003.jpg', '000004.jpg']
