"""
Speech-to-Text Module
Uses OpenAI Whisper to transcribe WAV, MP3, and M4A audio inputs.
"""

import whisper
import os
import sys

def transcribe_audio(audio_path, model_name="base"):
    """
    Transcribes the audio file located at audio_path using OpenAI Whisper.
    
    Parameters:
        audio_path (str): The absolute/relative path to the audio file.
        model_name (str): The size name of the Whisper model ('tiny', 'base', etc.)
        
    Returns:
        str: The transcribed text.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at: {audio_path}")
        
    print(f"[SpeechToText] Loading Whisper model: '{model_name}'...", flush=True)
    try:
        # Load the Whisper model (loads to CPU or GPU if available)
        model = whisper.load_model(model_name)
        
        print(f"[SpeechToText] Transcribing file: {os.path.basename(audio_path)}...", flush=True)
        result = model.transcribe(audio_path)
        
        transcription = result.get("text", "").strip()
        print(f"[SpeechToText] Transcription complete. Word count: {len(transcription.split())}", flush=True)
        return transcription
        
    except Exception as e:
        print(f"[SpeechToText] Error during transcription: {str(e)}", file=sys.stderr, flush=True)
        raise e
