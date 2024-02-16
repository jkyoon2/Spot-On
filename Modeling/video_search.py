import torch
import requests
import json, os
from typing import List
from run_on_video.run import run_example
from visualizer.visualize import overlay_and_plot
from PIL import Image

class VideoSearchModel:
    def __init__(self, pickle_path: str, image_dir: str, device, client_id, client_secret,url='https://openapi.naver.com/v1/papago/n2mt'):
        self.num_images = 1000
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.device = device
        # TODO 1: Initialize CG-DETR model
        # TODO 2: Initialize ImageSearchModel
        
    
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

    def search_moments(self, query_video: str, query_text: str, top_k: int = 5) -> str:
        # TODO 1: Translate the query_text to English using Papago API
        # TODO 2: Get top-k moments & scores from the CG-DETR model
        # TODO 3: Extract images of 10 frames & top-k momdents from the query_video
        # TODO 4: Visualize the scores (Movie CLIP and scores)

        query_text = self.translate(query_text)
        results = run_example(query_video, query_text)

        # Visualize the scores
        # Open frame.png and visualize the scores
        frame_image = Image.open('./visualizer/frame.png')
        figure_image = overlay_and_plot(results['n_parts_captures'], frame_image, results['pred_scores'])

        # Save the visualization
        # Remove the previous visualization
        if os.path.exists('./static/visualization.jpg'):
            os.remove('./static/visualization.jpg')
        figure_image.save('./static/visualization.jpg')

        # Save top-k moments
        for i, moment in enumerate(results['seconds_list_captures']):
            # Remove the previous image
            if os.path.exists(f'./static/{i}.jpg'):
                os.remove(f'./static/{i}.jpg')
            moment_image = Image.fromarray(moment)
            moment_image.save(f'./static/{i}.jpg')


        return_results = {}
        return_results['visualization'] = 'visualization.jpg'
        return_results['selectedMoments'] = [
            {'image': "0.jpg"},
            {'image': "1.jpg"},
            {'image': "2.jpg"},
            {'image': "3.jpg"},
            {'image': "4.jpg"}
        ]

        return results

    def search_images(self, query_image, query_text: str, top_k: int = 5) -> List[str]:
        # TODO 1: Use the ImageSearchModel to search images

        return ['000000.jpg', '000001.jpg', '000002.jpg', '000003.jpg', '000004.jpg']
