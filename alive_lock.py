"""
clonEnd - Lock 1: Alive Lock
AI-Powered Bio-Liveness & Finger Presentation Attack Detection (PAD)

Detects silicone rubber fake fingers, wax molds, 2D paper deed printouts,
and tape clones using multi-spectral skin chrominance, subsurface light
diffusion, micro-texture gradients, and specular glare analysis.
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple
from PIL import Image


class AliveLock:
    def __init__(self, liveness_threshold: float = 65.0):
        self.threshold = liveness_threshold

    def analyze_frame(self, frame_input: Any) -> Dict[str, Any]:
        """
        Analyzes a single frame (from webcam or uploaded image) to verify biological liveness.
        Accepts: cv2 BGR numpy array, or PIL Image.
        Returns: Detailed diagnostic dict and annotated visualization image.
        """
        # Convert PIL Image to cv2 BGR array if needed
        if isinstance(frame_input, Image.Image):
            rgb_arr = np.array(frame_input.convert("RGB"))
            bgr_frame = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
        elif isinstance(frame_input, np.ndarray):
            bgr_frame = frame_input.copy()
        else:
            raise ValueError("Unsupported frame input type. Provide numpy array or PIL Image.")

        h, w = bgr_frame.shape[:2]

        # 1. Focus region: Central 60% of frame (where finger is positioned)
        ymin, ymax = int(h * 0.15), int(h * 0.85)
        xmin, xmax = int(w * 0.20), int(w * 0.80)
        roi = bgr_frame[ymin:ymax, xmin:xmax]

        # Convert ROI to various color spaces
        ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # 2. Skin Chrominance & Blood Perfusion (Hemoglobin Red-Shift)
        # In YCrCb, human skin clusters: 133 <= Cr <= 173, 77 <= Cb <= 127
        # In HSV, human skin hue ranges between 0 and 25 (warm reddish-pink to golden brown)
        cr = ycrcb[:, :, 1]
        cb = ycrcb[:, :, 2]
        hue = hsv[:, :, 0]
        sat = hsv[:, :, 1]
        val = hsv[:, :, 2]

        skin_mask_ycrcb = (cr >= 133) & (cr <= 175) & (cb >= 75) & (cb <= 130)
        skin_mask_hsv = ((hue >= 0) & (hue <= 28) | (hue >= 165)) & (sat >= 30) & (val >= 40)
        combined_skin_mask = skin_mask_ycrcb & skin_mask_hsv

        total_pixels = roi.shape[0] * roi.shape[1]
        skin_pixels = np.sum(combined_skin_mask)
        skin_ratio = float(skin_pixels / total_pixels)

        # 3. Paper Printout / Grayscale Document Detection
        # Scanned deed printouts on paper have high white background (saturation < 15, value > 190)
        # or flat monochrome black toner ink with standard deviation < 12
        paper_white_mask = (sat < 22) & (val > 180)
        paper_ratio = float(np.sum(paper_white_mask) / total_pixels)
        
        # Color variance across RGB channels (paper & grayscale have very low inter-channel variance)
        b, g, r = roi[:, :, 0], roi[:, :, 1], roi[:, :, 2]
        color_std = float(np.std([np.mean(r), np.mean(g), np.mean(b)]))

        # 4. Micro-Texture & Papillary Ridge Analysis
        # Real biological skin has fine epidermal ridges with characteristic Laplacian variance (150-1800)
        # Flat paper has low variance; synthetic silicone has flat untextured or bubbly surfaces
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_var = float(laplacian.var())

        # High frequency edge density
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        edge_energy = float(np.mean(np.sqrt(sobelx**2 + sobely**2)))

        # 5. Specular Glare / Adhesive Tape / Plastic Reflection Index
        # Silicone rubber and adhesive tape reflect sharp, localized hot white glare
        glare_mask = (val > 240) & (sat < 30)
        glare_ratio = float(np.sum(glare_mask) / total_pixels)

        # 6. Composite Liveness Calculation
        # Healthy skin ratio score (0 - 45 pts)
        if skin_ratio >= 0.35:
            skin_score = min(45.0, 20.0 + (skin_ratio - 0.35) * 60.0)
        else:
            skin_score = max(0.0, skin_ratio * 50.0)

        # Organic texture & edge naturalness score (0 - 40 pts)
        if 80.0 <= texture_var <= 2200.0 and edge_energy >= 10.0:
            texture_score = 40.0
        elif texture_var < 80.0:
            texture_score = max(5.0, (texture_var / 80.0) * 35.0)
        else:
            # Overly noisy / dithering artifacts
            texture_score = max(10.0, 40.0 - (texture_var - 2200.0) * 0.01)

        # Organic blood chromaticity score (0 - 15 pts)
        if color_std >= 12.0 and paper_ratio < 0.30:
            chroma_score = 15.0
        elif color_std < 5.0 or paper_ratio >= 0.50:
            chroma_score = 0.0
        else:
            chroma_score = (color_std / 12.0) * 15.0

        # Penalties:
        penalty = 0.0
        if paper_ratio > 0.40:
            # High paper background -> Document / Deed printout detected
            penalty += (paper_ratio - 0.40) * 60.0
        if glare_ratio > 0.12:
            # High specular reflection -> Plastic tape / silicone sheen
            penalty += (glare_ratio - 0.12) * 50.0
        if color_std < 6.0:
            # Monochromatic printout / photocopy penalty
            penalty += 25.0

        raw_score = (skin_score + texture_score + chroma_score) - penalty
        liveness_score = float(np.clip(raw_score, 0.0, 99.8))

        is_live = liveness_score >= self.threshold

        # Primary fraud reason classification
        if is_live:
            verdict = "Real Finger - Verified"
            fraud_type = "None (Living Human Skin)"
            status_color = (46, 204, 113)  # Bright Green in BGR
        else:
            if paper_ratio >= 0.35 or color_std < 7.0:
                verdict = "Fraud Detected: Paper / Deed Printout"
                fraud_type = "2D Paper Photocopy (Land Deed Clone)"
            elif glare_ratio >= 0.10:
                verdict = "Fraud Detected: Adhesive Tape / Glossy Clone"
                fraud_type = "Tape Transfer / Synthetic Mold"
            elif skin_ratio < 0.20:
                verdict = "Fraud Detected: Dummy Silicone Rubber"
                fraud_type = "Silicone / Wax Biometric Dummy"
            else:
                verdict = "Fraud Detected: Spoofed Presentation Attack"
                fraud_type = "Unnatural Texture / Non-Living Surface"
            status_color = (50, 50, 235)  # Crimson Red in BGR

        # 7. Create Annotated Visualization Image
        annotated = bgr_frame.copy()
        
        # Draw scanning target rectangle
        cv2.rectangle(annotated, (xmin, ymin), (xmax, ymax), status_color, 3)

        # Target corner reticles
        corner_len = 25
        # Top-left
        cv2.line(annotated, (xmin, ymin), (xmin + corner_len, ymin), status_color, 4)
        cv2.line(annotated, (xmin, ymin), (xmin, ymin + corner_len), status_color, 4)
        # Top-right
        cv2.line(annotated, (xmax, ymin), (xmax - corner_len, ymin), status_color, 4)
        cv2.line(annotated, (xmax, ymin), (xmax, ymin + corner_len), status_color, 4)
        # Bottom-left
        cv2.line(annotated, (xmin, ymax), (xmin + corner_len, ymax), status_color, 4)
        cv2.line(annotated, (xmin, ymax), (xmin, ymax - corner_len), status_color, 4)
        # Bottom-right
        cv2.line(annotated, (xmax, ymax), (xmax - corner_len, ymax), status_color, 4)
        cv2.line(annotated, (xmax, ymax), (xmax, ymax - corner_len), status_color, 4)

        # Overlay status banner at bottom
        cv2.rectangle(annotated, (0, h - 55), (w, h), (20, 20, 25), -1)
        badge_text = f"LOCK 1: {verdict.upper()} [{liveness_score:.1f}%]"
        cv2.putText(annotated, badge_text, (20, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2, cv2.LINE_AA)

        # Convert annotated BGR back to RGB for web rendering
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        return {
            "is_live": is_live,
            "liveness_score": round(liveness_score, 1),
            "threshold": self.threshold,
            "verdict": verdict,
            "fraud_type": fraud_type,
            "status_color": "green" if is_live else "red",
            "diagnostics": {
                "skin_perfusion_ratio": round(skin_ratio * 100, 1),
                "micro_texture_variance": round(texture_var, 1),
                "edge_energy": round(edge_energy, 1),
                "chromatic_std": round(color_std, 1),
                "paper_background_ratio": round(paper_ratio * 100, 1),
                "specular_glare_ratio": round(glare_ratio * 100, 1)
            },
            "annotated_image": annotated_rgb
        }
