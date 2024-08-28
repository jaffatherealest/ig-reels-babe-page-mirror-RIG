import subprocess
import os

# Set environment variables (adjust the paths as needed)
os.environ['TVAI_MODEL_DATA_DIR'] = r'C:\Users\fymfo\Documents\Topaz VideoAI Projects'  # Ensure this directory exists and has enough space
os.environ['TVAI_MODEL_DIR'] = r'C:\ProgramData\Topaz Labs LLC\Topaz Video AI\models'  # Correct path to the model directory

# Path to the FFmpeg executable integrated with Topaz Video AI
ffmpeg_exe_path = r"C:\Program Files\Topaz Labs LLC\Topaz Video AI\ffmpeg.exe"

def upscale_video(input_temp_path, output_temp_path):
    command = [
        ffmpeg_exe_path,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i", input_temp_path,
        "-sws_flags", "spline+accurate_rnd+full_chroma_int",
        "-filter_complex",
        "[0:v]format=yuv420p,scale=in_color_matrix=bt709:out_color_matrix=bt709[tvai];[tvai]tvai_fi=model=chf-3:slowmo=1:rdt=0.01:fps=60:device=0:vram=1:instances=1,tvai_up=model=ghq-5:scale=0:w=2160:h=3840:device=0:vram=1:instances=1,scale=w=2160:h=3840:flags=lanczos:threads=0[vf]",
        "-map", "[vf]",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:v", "h264_nvenc",
        "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-g", "30",
        "-preset", "p7",
        "-tune", "hq",
        "-rc", "vbr",
        "-b:v", "100M",
        "-maxrate", "100M",
        "-bufsize", "200M",
        "-map", "0:a?",
        # "-map_metadata:s:a:0", "0:s:a:0",
        "-c:a", "aac",
        "-b:a", "128k",
        "-map_metadata", "0",
        "-map_metadata:s:v", "0:s:v",
        "-movflags", "frag_keyframe+empty_moov+delay_moov+use_metadata_tags+write_colr",
        "-bf", "0",
        "-metadata", "description=Iphone 13 - Pro",
        output_temp_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully processed: {input_temp_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_temp_path}: {e}")
        print(f"Command output: {e.output}")
        raise e