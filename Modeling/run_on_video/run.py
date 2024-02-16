import torch

from run_on_video.data_utils import ClipFeatureExtractor
from run_on_video.model_utils import build_inference_model
from utils.tensor_utils import pad_sequences_1d
from cg_detr.span_utils import span_cxw_to_xx
from utils.basic_utils import l2_normalize_np_array, modify_length, capture_video
import torch.nn.functional as F
import numpy as np
import subprocess
import os
import json
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import ffmpeg

def load_jsonl(filename):
    with open(filename, "r") as f:
        return [json.loads(l.strip("\n")) for l in f.readlines()]

class CGDETRPredictor:
    def __init__(self, ckpt_path, clip_model_name_or_path="ViT-B/32", device="cuda", captured_path='./static/captured_images'):
        self.clip_len = 2  # seconds
        self.device = device
        self.captured_path = captured_path
        print("Loading feature extractors...")
        self.feature_extractor = ClipFeatureExtractor(
            framerate=1/self.clip_len, size=224, centercrop=True,
            model_name_or_path=clip_model_name_or_path, device=device
        )
        print("Loading trained CG-DETR model...")
        self.model = build_inference_model(ckpt_path).to(self.device)

    @torch.no_grad()
    def localize_moment(self, video_path, query_list):
        """
        Args:
            video_path: str, path to the video file
            query_list: List[str], each str is a query for this video
        """
        # construct model inputs
        n_query = len(query_list)
        video_feats = self.feature_extractor.encode_video(video_path)
        video_feats = F.normalize(video_feats, dim=-1, eps=1e-5)
        n_frames = len(video_feats)
        # add tef
        tef_st = torch.arange(0, n_frames, 1.0) / n_frames
        tef_ed = tef_st + 1.0 / n_frames
        tef = torch.stack([tef_st, tef_ed], dim=1).to(self.device)  # (n_frames, 2)
        video_feats = torch.cat([video_feats, tef], dim=1)
        assert n_frames <= 75, "The positional embedding of this pretrained CGDETR only support video up " \
                               "to 150 secs (i.e., 75 2-sec clips) in length"
        video_feats = video_feats.unsqueeze(0).repeat(n_query, 1, 1)  # (#text, T, d)
        video_mask = torch.ones(n_query, n_frames).to(self.device)
        query_feats = self.feature_extractor.encode_text(query_list)  # #text * (L, d)
        query_feats, query_mask = pad_sequences_1d(
            query_feats, dtype=torch.float32, device=self.device, fixed_length=None)
        query_feats = F.normalize(query_feats, dim=-1, eps=1e-5)
        model_inputs = dict(
            src_vid=video_feats,
            src_vid_mask=video_mask,
            src_txt=query_feats,
            src_txt_mask=query_mask,
            vid=None,
            qid=None
        )

        # decode outputs
        outputs = self.model(**model_inputs)
        # #moment_queries refers to the positional embeddings in CGDETR's decoder, not the input text query
        prob = F.softmax(outputs["pred_logits"], -1)  # (batch_size, #moment_queries=10, #classes=2)
        scores = prob[..., 0]  # * (batch_size, #moment_queries)  foreground label is 0, we directly take it
        pred_spans = outputs["pred_spans"]  # (bsz, #moment_queries, 2)
        _saliency_scores = outputs["saliency_scores"].half()  # (bsz, L)
        saliency_scores = []
        valid_vid_lengths = model_inputs["src_vid_mask"].sum(1).cpu().tolist()
        for j in range(len(valid_vid_lengths)):
            _score = _saliency_scores[j, :int(valid_vid_lengths[j])].tolist()
            _score = [round(e, 4) for e in _score]
            saliency_scores.append(_score)

        # compose predictions
        predictions = []
        video_duration = n_frames * self.clip_len
        for idx, (spans, score) in enumerate(zip(pred_spans.cpu(), scores.cpu())):
            spans = span_cxw_to_xx(spans) * video_duration
            # # (#queries, 3), [st(float), ed(float), score(float)]
            cur_ranked_preds = torch.cat([spans, score[:, None]], dim=1).tolist()
            cur_ranked_preds = sorted(cur_ranked_preds, key=lambda x: x[2], reverse=True)
            cur_ranked_preds = [[float(f"{e:.4f}") for e in row] for row in cur_ranked_preds]
            cur_query_pred = dict(
                query=query_list[idx],  # str
                vid=video_path,
                pred_relevant_windows=cur_ranked_preds,  # List([st(float), ed(float), score(float)])
                pred_saliency_scores=saliency_scores[idx]  # List(float), len==n_frames, scores for each frame
            )
            predictions.append(cur_query_pred)

        return predictions

def run_example(youtube_url='', desired_query='', video_path=''):

    '''
    1) If you want to use the custom data, leave the url empty
    '''
    '''
    2) If you want to run with a video from youtube, please enter the youtube_url, [st, ed] in seconds, and custom query
    # Maximum duration is 150 secs or lower. Recommend to use less than 150 secs.
    youtube_url = 'https://www.youtube.com/watch?v=geklhsKfw7I'
    vid_st_sec, vid_ed_sec = 60.0, 205.0
    desired_query = 'Girls having fun out side shop'
    '''
    # load example data
    from utils.basic_utils import load_jsonl

    if youtube_url != '':
        # vid = info['vid'] # "vid": "NUsG9BgSes0_210.0_360.0"
        queries = []
        queries.append({})
        file_name = youtube_url.split('/')[-1][8:] + '.mp4'
        
        # Remove the video if it already exists
        if os.path.exists(os.path.join('run_on_video/example', file_name)):
            os.remove(os.path.join('run_on_video/example', file_name))
        if os.path.exists(os.path.join('run_on_video/example', 'output.mp4')):
            os.remove(os.path.join('run_on_video/example', 'output.mp4'))
        
        # Download video from youtube
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.get_highest_resolution()
            video_path = os.path.join('./run_on_video/example', file_name)
            stream.download(output_path='./run_on_video/example', filename=file_name)
        except:
            print('Error downloading video')
            exit(1)
        
        # Modify the length of the video
        video_path_new_length = os.path.join("run_on_video/example", "output.mp4")
        modify_length(video_path, video_path_new_length, new_length=145.0)
        queries[0]['query'] = desired_query
        video_path = video_path_new_length
        
    else:
        # Remove output file if it already exists
        if os.path.exists(os.path.join('run_on_video/example', 'output.mp4')):
            os.remove(os.path.join('run_on_video/example', 'output.mp4'))
        
        # Modify the length of the video
        video_path_new_length = os.path.join("run_on_video/example", "output.mp4")
        modify_length(video_path, video_path_new_length, new_length=145.0)
        video_path = video_path_new_length
        queries = []
        queries.append({})
        queries[0]['query'] = desired_query
    
    query_text_list = [e["query"] for e in queries]
    ckpt_path = "run_on_video/CLIP_ckpt/qvhighlights_onlyCLIP/model_best.ckpt"

    # run predictions
    print("Build models...")
    clip_model_name_or_path = "ViT-B/32"
    # clip_model_name_or_path = "tmp/ViT-B-32.pt"
    cg_detr_predictor = CGDETRPredictor(
        ckpt_path=ckpt_path,
        clip_model_name_or_path=clip_model_name_or_path,
        device="cuda"
    )
    print("Run prediction...")
    predictions = cg_detr_predictor.localize_moment(
        video_path=video_path, query_list=query_text_list)
    
    # Results
    results = {}
    results['query'] = queries[0]['query']
    results['topk_moments'] = (np.argsort(predictions[0]['pred_saliency_scores'])[::-1][:5] * 2).tolist()
    results['pred_scores'] = predictions[0]['pred_saliency_scores']
    
    # TODO: Currently, it saves the captured images of the top-5 moments. It should be changed to return the images.
    
    captued_images = capture_video(video_path, 10, results['topk_moments'])
    results['seconds_list_captures'] = captued_images['seconds_list_captures']
    results['n_parts_captures'] = captued_images['n_parts_captures']
    
    print(f"Results: {results}")
    
    return results



if __name__ == "__main__":
    youtube_url = 'https://youtu.be/QTqvR6vVyfc?si=38hl4xafh7KWRbZX'
    run_example(youtube_url, 'A woman is walking on the street.')
    # run_example(desired_query='A woman is walking on the street.', video_path='run_on_video/example/yfc?si=38hl4xafh7KWRbZX.mp4')
