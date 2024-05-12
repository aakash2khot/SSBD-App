import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import io
from m1 import SSBDModel1
from m2 import load_ssbd_model2, m2_identify
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
import cv2 
from torchsummary import summary
from torchvision.transforms import ToTensor
from PIL import Image
"""
    Arguments for the M1 model
"""
M1_PARAMS = dict(
    in_channels = 3, 
    intermediate = 16, 
    out_channels = 8, 
    kernel_size = [3, 3, 3], 
    strides = [1, 1, 1], 
    pooling_size = [1, 3, 3], 
    pooling_strides = [1, 3, 3], 
    size_1 = 128, 
    size_2 = 64, 
    size_3 = 16
)
ID2ACTION = ["Noclass", "Armflapping", "Headbanging", "Spinning"]

def extract_frames(video_path, num_frames):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    return frames

# Function to preprocess frames
def preprocess_frames(frames):
    preprocess = transforms.Compose([
        transforms.ToPILImage(),              # Convert numpy array to PIL Image
        transforms.Resize((100, 100)),          # Resize to desired dimensions
        transforms.ToTensor(),                # Convert to tensor
    ])
    preprocessed_frames = torch.stack([preprocess(frame) for frame in frames], dim=1)  # Stack along the frame dimension
    # print(preprocessed_frames.shape)
    return preprocessed_frames

"""
    Pipeline Code. Outputs the exact action name out of ID2ACTION
"""
def detect_actions(video_path):
    results = []
    m1 = SSBDModel1(**M1_PARAMS)
    m2 = load_ssbd_model2()
    
    # video = prefetch_call(video_path) # TODO
    frames = extract_frames(video_path, 40)
    frames = preprocess_frames(frames)
    video = frames.unsqueeze(0)  
    print(video.shape)
    m1.eval()
    prob_action = F.sigmoid(m1(video))
    action_id = -1
    
    if prob_action > 0.001:
        print("action!")
        # m2_prediction = m2_identify(m2, video_path)
        # action_id = np.argmax(m2_prediction, axis = 1)
        action_id = np.argmax(m2_identify(m2, video_path), axis = 1)
    # print(action_id)    
    return ID2ACTION[action_id[0] + 1]
    
# print(detect_actions("v2.mp4"))

# def preprocess_frames(frames):
#     preprocess = transforms.Compose([
#         transforms.ToPILImage(),           # Convert numpy array to PIL Image
#         transforms.Resize((100, 100)),     # Resize to desired dimensions
#         transforms.ToTensor(),             # Convert to tensor
#     ])
#     preprocessed_frames = torch.stack([preprocess(frame) for frame in frames], dim=1)  # Stack along the frame dimension
#     return preprocessed_frames

# def extract_frames(video, num_frames):
#     frame_count = int(video.shape[0])
#     frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)

#     frames = []
#     for idx in frame_indices:
#         frame = video[idx]
#         frames.append(frame)
#     return frames
# def decode_video(video_data):
#     try:
#         nparr = np.frombuffer(video_data, np.uint8)
#         video = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         if video is None:
#             raise Exception("Failed to decode video data")
#         return video
#     except Exception as e:
#         print(f"Error decoding video data: {str(e)}")
#         return None
    
# def detect_actions(video_data):
#     print("Starting detect_actions function...")
#     results = []

#     # Decode video data
#     video = decode_video(video_data)
#     if video is None:
#         return 'Error: Failed to decode video data'

#     print("Video data decoded")

#     try:
#         # Extract frames from the video
#         frames = extract_frames(video, 40)
#         print("Frames extracted")

#         # Preprocess frames
#         frames = preprocess_frames(frames)
#         print("Frames preprocessed")
#     except Exception as e:
#         print(f"Error processing frames: {str(e)}")
#         return 'Error processing frames'

#     # Perform action detection
#     try:
#         # Perform action detection
#         m1 = SSBDModel1(**M1_PARAMS)
#         m2 = load_ssbd_model2()
#         m1.eval()

#         # Assuming m2_identify is defined elsewhere
#         prob_action = F.sigmoid(m1(frames.unsqueeze(0)))
#         action_id = -1
        
#         if prob_action > 0.5:
#             action_id = np.argmax(m2_identify(video_data), axis=1)
        
#         print("Actions detected")
#         return ID2ACTION[action_id + 1]
#     except Exception as e:
#         print(f"Error detecting actions: {str(e)}")
#         return 'Error detecting actions'