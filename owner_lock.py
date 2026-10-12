"""
clonEnd - Lock 3: Owner Lock
Tamil Voice IVR Verification for Basic 2G Keypad Phones

Generates authentic spoken Tamil voice prompts via gTTS and handles
simulated DTMF interactive voice response (IVR) without requiring a smartphone,
internet connection, or the mAadhaar app.
"""

import os
import hashlib
from typing import Dict, Any, Optional
from gtts import gTTS


class OwnerLock:
    def __init__(self, audio_cache_dir: Optional[str] = None):
        if audio_cache_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            audio_cache_dir = os.path.join(base_dir, "assets", "audio")
        
        self.cache_dir = audio_cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate_tamil_voice_prompt(self,
                                    aadhaar_masked: str,
                                    kiosk_city: str,
                                    amount: int,
                                    beneficiary_name: str) -> Dict[str, Any]:
        """
        Generates or retrieves cached Tamil voice prompt audio.
        Returns the text script and local mp3 file path.
        """
        # Spoken Tamil IVR script
        tamil_script = (
            f"வணக்கம் {beneficiary_name}! உங்கள் ஆதார் எண் {aadhaar_masked} பயன்படுத்தி, "
            f"{kiosk_city} வங்கி மித்ரா மையத்தில் ரூபாய் {amount} பணம் எடுக்க முயற்சி செய்யப்படுகிறது. "
            f"நீங்கள் தான் பணம் எடுக்கிறீர்கள் என்றால் ஒன்று அழுத்தவும். "
            f"நீங்கள் இல்லை என்றால் ஒன்பது அழுத்தவும்."
        )

        english_transcript = (
            f"Greetings {beneficiary_name}! An AePS cash withdrawal of Rs.{amount} "
            f"is being attempted at {kiosk_city} Micro-ATM using your Aadhaar {aadhaar_masked}. "
            f"If you are making this withdrawal, press 1. If NOT you, press 9."
        )

        # Unique hash for caching
        hash_key = hashlib.md5(f"{aadhaar_masked}_{kiosk_city}_{amount}_{beneficiary_name}".encode('utf-8')).hexdigest()[:10]
        audio_filename = f"ivr_prompt_{hash_key}.mp3"
        audio_filepath = os.path.join(self.cache_dir, audio_filename)

        # Generate audio file if not already cached
        if not os.path.exists(audio_filepath):
            try:
                tts = gTTS(text=tamil_script, lang="ta", slow=False)
                tts.save(audio_filepath)
            except Exception as e:
                # If network is unavailable, create a fallback or report error
                audio_filepath = None

        return {
            "tamil_script": tamil_script,
            "english_transcript": english_transcript,
            "audio_filepath": audio_filepath,
            "filename": audio_filename
        }

    def verify_ivr_response(self, dtmf_input: Optional[str]) -> Dict[str, Any]:
        """
        Evaluates the user's DTMF keypad input on the 2G phone.
        '1' -> Approved by genuine owner
        '9' -> Rejected (Owner indicates fraud)
        None / Other -> No response / Timeout
        """
        if dtmf_input == "1":
            return {
                "is_confirmed": True,
                "status": "APPROVED",
                "verdict": "Owner Confirmed via Tamil Voice Call",
                "status_color": "green",
                "dtmf_key": "1",
                "details": "Customer pressed '1' on phone keypad. Authorized legitimate cash withdrawal."
            }
        elif dtmf_input == "9":
            return {
                "is_confirmed": False,
                "status": "REJECTED_BY_OWNER",
                "verdict": "Fraud Reported: Owner Pressed 9 (Reject)",
                "status_color": "red",
                "dtmf_key": "9",
                "details": "Victim answered keypad call and pressed '9' (Unauthorized). Scam immediately averted!"
            }
        elif dtmf_input == "TIMEOUT" or dtmf_input is None:
            return {
                "is_confirmed": False,
                "status": "NO_RESPONSE",
                "verdict": "Fraud Alert: Voice Call Unanswered / Timeout",
                "status_color": "red",
                "dtmf_key": "None",
                "details": "Registered phone did not answer the IVR call within the 30-second security window."
            }
        else:
            return {
                "is_confirmed": False,
                "status": "INVALID_KEY",
                "verdict": "Invalid DTMF Key Pressed",
                "status_color": "red",
                "dtmf_key": str(dtmf_input),
                "details": f"Unknown key '{dtmf_input}' pressed. Transaction held for safety."
            }
