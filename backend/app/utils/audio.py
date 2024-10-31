from pathlib import Path
from pydub import AudioSegment
import os

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def normalize_audio(input_path: str, output_path: str = None) -> str:
    """Normalize audio file to 128Kbps CBR, 44.1KHz, 2 channels"""
    if not output_path:
        output_path = input_path.rsplit(".", 1)[0] + "_normalized.mp3"
        
    audio = AudioSegment.from_file(input_path)
    
    # Convert to stereo
    if audio.channels == 1:
        audio = audio.set_channels(2)
    
    # Set sample rate to 44.1KHz
    audio = audio.set_frame_rate(44100)
    
    # Export with specific bitrate
    audio.export(
        output_path,
        format="mp3",
        bitrate="128k",
        parameters=["-c:a", "libmp3lame"]
    )
    
    return output_path

def generate_audio_from_template(template_path: str, output_path: str) -> str:
    """Generate audio track from template"""
    # For now, just copy the template file
    # In the future, this could be replaced with actual text-to-speech
    audio = AudioSegment.from_file(template_path)
    audio.export(output_path, format="mp3")
    return output_path

def save_uploaded_file(file, filename: str) -> str:
    """Save uploaded file and return the path"""
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return str(file_path)

def delete_file(file_path: str) -> None:
    """Delete file if it exists"""
    try:
        os.remove(file_path)
    except OSError:
        pass # File doesn't exist or other error