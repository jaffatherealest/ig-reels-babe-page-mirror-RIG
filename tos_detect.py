import tempfile
import os
import io
from google.cloud import vision
import subprocess

from config import (
    SERVICE_ACCOUNT_PATH
) # running this import to make sure the config.py is run and local var is set service account path

def extract_frames_from_video(file_io, frame_rate=1):
    # Create a temporary file for the video
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
        temp_video.write(file_io.getbuffer())
        temp_video_path = temp_video.name

    frame_files = []
    try:
        # Build the ffmpeg command
        output_pattern = 'frame_%04d.png'
        command = [
            'ffmpeg',
            '-i', temp_video_path,
            '-vf', f'fps={frame_rate}',
            output_pattern
        ]

        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Collect all the frame files
        frame_files = sorted([f for f in os.listdir() if f.startswith('frame_') and f.endswith('.png')])

    except subprocess.CalledProcessError as e:
        print(f"Error during frame extraction: {e}")
    finally:
        os.remove(temp_video_path)  # Clean up the temporary video file

    return frame_files

def detect_text_in_frames(frame_files):
    client = vision.ImageAnnotatorClient()
    for frame_file in frame_files:
        with io.open(frame_file, 'rb') as image:
            content = image.read()
            image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            print(f"Text detected in {frame_file}. Skipping video.")
            return True  # Text detected
    return False  # No text detected

def cleanup_files(file_list):
    for file in file_list:
        os.remove(file)
