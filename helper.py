"""
Filler Word Detection Module
Identifies and counts vocal disfluency markers (fillers) such as 'um', 'uh', 'like', etc.
Computes filler word counts and disfluency ratios relative to total words.
"""

import re
import sys

def detect_filler_words(text):
    """
    Detects and analyzes the frequency of common filler words/phrases in the transcription.
    Filler words detected: um, uh, like, actually, basically, you know, okay, so, hmm.
    
    Parameters:
        text (str): The transcribed spoken text.
        
    Returns:
        dict: A dictionary containing:
            - filler_count (int): Total number of detected filler words.
            - filler_ratio (float): Ratio of filler words to total words.
            - details (dict): Detailed occurrences of each specific filler word.
            - total_words (int): Total words in transcription.
    """
    fillers = ['um', 'uh', 'like', 'actually', 'basically', 'you know', 'okay', 'so', 'hmm']
    
    if not text or not text.strip():
        print("[FillerDetector] Empty transcription provided. Returning zero counts.")
        return {
            "filler_count": 0,
            "filler_ratio": 0.0,
            "details": {f: 0 for f in fillers},
            "total_words": 0
        }
        
    # Clean up input text for uniform matching (lowercase and strip punctuation)
    text_cleaned = text.lower()
    
    # Simple word counting (tokenization via regex word boundaries)
    words = re.findall(r'\b[a-zA-Z\']+\b', text_cleaned)
    total_words = len(words)
    
    filler_count = 0
    filler_details = {f: 0 for f in fillers}
    
    try:
        # 1. Search for multi-word phrases first to avoid duplicate counting (e.g. "you know")
        for filler in fillers:
            if ' ' in filler:
                # Compile a regex with word boundaries around the phrase
                pattern = rf'\b{re.escape(filler)}\b'
                matches = re.findall(pattern, text_cleaned)
                count = len(matches)
                filler_details[filler] = count
                filler_count += count
                # We count "you know" as one disfluency instance. 
                # In terms of simple word ratio, we can adjust the total word count if we want, 
                # but dividing by standard word count is conventional and clear.
                
        # 2. Search for single word fillers
        for filler in fillers:
            if ' ' not in filler:
                pattern = rf'\b{re.escape(filler)}\b'
                matches = re.findall(pattern, text_cleaned)
                count = len(matches)
                filler_details[filler] = count
                filler_count += count
                
        # 3. Calculate filler disfluency ratio
        filler_ratio = filler_count / total_words if total_words > 0 else 0.0
        
        print(f"[FillerDetector] Counted {filler_count} filler words out of {total_words} total words. "
              f"Ratio: {filler_ratio:.2%} ({filler_ratio:.4f})", flush=True)
              
        return {
            "filler_count": filler_count,
            "filler_ratio": filler_ratio,
            "details": filler_details,
            "total_words": total_words
        }
        
    except Exception as e:
        print(f"[FillerDetector] Error during filler word detection: {str(e)}", file=sys.stderr, flush=True)
        raise e
