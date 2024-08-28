import subprocess
import tempfile
import shutil
import os

def apply_mirror_video(input_io, output_io):
    try:
        print(f'Starting video processing.')

        # Create a temporary file for input
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            temp_input.write(input_io.getbuffer())
            temp_input_path = temp_input.name
        
        # Create a temporary file for output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
            temp_output_path = temp_output.name

        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output files without asking
            '-i', temp_input_path,  # Input file
            '-vf', 'hflip,scale=1080:1920',  # Video filters: horizontal flip and scaling
            '-acodec', 'copy',  # Copy audio
            '-vcodec', 'libx264',  # Use the H.264 video codec
            '-pix_fmt', 'yuv420p',  # Pixel format, ensure it's yuv420p for maximum compatibility
            '-profile:v', 'high',  # Use high profile for better compression efficiency
            '-level', '4.1',  # Set level to 4.1 to support resolutions up to 1080p on older devices
            '-preset', 'medium',  # Preset for encoding speed/quality trade-off (medium is a good default)
            '-crf', '22',  # Constant Rate Factor for quality control
            '-f', 'mp4',  # Specify the container format as MP4
            temp_output_path  # Output file
        ]

        # Execute the FFmpeg command and capture stdout and stderr
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Logging the output
        print(f'FFmpeg stdout: {result.stdout}')
        print(f'Successfully processed video.')

        # Read the temporary output file and write to the output_io
        with open(temp_output_path, 'rb') as f:
            shutil.copyfileobj(f, output_io)

    except subprocess.CalledProcessError as e:
        # Log the stderr and stdout from subprocess
        print(f'FFmpeg subprocess error.')
        print(f'Stderr: {e.stderr}')
        print(f'Stdout: {e.stdout}')
        raise
    except Exception as e:
        # Log unexpected exceptions
        print(f'Unexpected error processing file: {e}')
        raise
    finally:
        # Clean up temporary files
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)
