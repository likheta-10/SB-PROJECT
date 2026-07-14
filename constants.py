"""
Audio Feature Extraction Module
Computes pause ratio, RMS energy, speaking/silence duration, speech rate, and confidence metrics
using Librosa and SoundFile libraries.
"""

import librosa
import soundfile as sf
import numpy as np
import sys
import os

def extract_audio_features(audio_path, transcription="", top_db_silence=25):
    """
    Analyzes an audio file to extract acoustic properties related to speaking style and audio quality.
    
    Parameters:
        audio_path (str): Path to the audio file.
        transcription (str): The transcription text, used to compute speech rate.
        top_db_silence (int): Threshold (in dB) below peak to consider as silence.
        
    Returns:
        dict: Extracted audio features.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at: {audio_path}")
        
    print(f"[AudioFeatures] Analyzing audio: {os.path.basename(audio_path)} using Librosa...", flush=True)
    try:
        # Load audio file (with original sample rate for accurate sound analysis)
        y, sr = librosa.load(audio_path, sr=None)
        
        # 1. Total Audio Duration
        duration = float(librosa.get_duration(y=y, sr=sr))
        if duration == 0.0:
            raise ValueError("Audio duration is 0 seconds.")
            
        # 2. RMS (Root-Mean-Square) Energy
        # Computes energy for each frame. Gives a metric of speaking loudness/presence.
        rms = librosa.feature.rms(y=y)
        mean_rms = float(np.mean(rms))
        
        # 3. Speaking vs Silence Durations
        # librosa.effects.split splits audio into non-silent intervals.
        # top_db=25 means anything 25 decibels below reference is deemed silent.
        non_silent_intervals = librosa.effects.split(y, top_db=top_db_silence)
        
        speaking_duration = 0.0
        for start, end in non_silent_intervals:
            speaking_duration += (end - start) / sr
            
        # Avoid exceeding total duration due to floating point arithmetic
        speaking_duration = min(duration, speaking_duration)
        silence_duration = max(0.0, duration - speaking_duration)
        
        # 4. Pause Ratio
        # Fraction of the speaking audio that was spent in silent pauses
        pause_ratio = silence_duration / duration if duration > 0 else 0.0
        
        # 5. Speech Rate (words per speaking minute)
        words_count = len(transcription.split()) if transcription else 0
        speaking_minutes = speaking_duration / 60.0
        speech_rate = (words_count / speaking_minutes) if speaking_minutes > 0 else 0.0
        
        # 6. Confidence Metric
        # Estimate signal quality (Signal-to-Noise Ratio proxy) based on standard deviation of RMS Energy,
        # where higher background noise or audio clipping lowers the estimated confidence.
        # We also factor in a reasonable audio level checking.
        if mean_rms < 0.001:
            confidence_metric = 0.3  # Too quiet / empty audio
        elif mean_rms > 0.4:
            confidence_metric = 0.6  # High clipping/noise
        else:
            # High quality signal typically has clean peaks and silent sections (dynamic variance)
            std_rms = float(np.std(rms))
            snr_proxy = std_rms / (mean_rms + 1e-6)
            # Normalize to a percentage-like confidence score [0.0 - 1.0]
            confidence_metric = float(min(1.0, max(0.4, 0.5 + snr_proxy * 0.3)))
            
        print(f"[AudioFeatures] Analysis completed successfully: "
              f"Duration={duration:.2f}s, RMS={mean_rms:.4f}, PauseRatio={pause_ratio * 100:.2f}%, "
              f"SpeechRate={speech_rate:.1f} WPM, Confidence={confidence_metric:.2f}", flush=True)
              
        return {
            "duration": duration,
            "rms_energy": mean_rms,
            "speaking_duration": speaking_duration,
            "silence_duration": silence_duration,
            "pause_ratio": pause_ratio,
            "speech_rate": speech_rate,
            "confidence_metric": confidence_metric
        }
        
    except Exception as e:
        print(f"[AudioFeatures] Error during audio analysis: {str(e)}", file=sys.stderr, flush=True)
        raise e
