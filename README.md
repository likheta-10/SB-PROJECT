"""
Constants Configuration
Declares globally referenced variables and static mappings.
"""

# Allowed extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

# Complete checklist of filler words/hesitation markers
FILLER_WORDS = [
    'um', 'uh', 'like', 'actually', 'basically', 
    'you know', 'okay', 'so', 'hmm'
]

# Classification tiers
CLASS_STRONG = "Strong Understanding"
CLASS_MODERATE = "Moderate Understanding"
CLASS_POOR = "Poor Understanding"

# Metric Descriptions for reporting
DESCRIPTIONS = {
    "similarity": "Measures vocabulary overlap and semantic correctness compared to the ideal textbook answer.",
    "pause_ratio": "Assesses fluency. High silence suggests hesitation or memory recall delay.",
    "rms_energy": "Corresponds to acoustic amplitude/volume. Low energy signals whispering or voice trembling.",
    "speech_rate": "Speaking speed (Words Per Minute). Normal conversing rate is 110-150 WPM.",
    "confidence_metric": "Combines signal amplitude and voice dynamics to index confidence."
}
