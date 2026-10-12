# 🛡️ clonEnd: Stopping Aadhaar Fingerprint Cloning Scams

> **Domain:** Cybersecurity & Digital India (AePS Financial Fraud Prevention)  
> **Problem:** Scammers clone thumbprints from online government land deed PDFs into silicone/rubber stamps, then steal cash at rural Bank Mitra (Micro-ATM) shops with no OTP.  
> **Solution:** A 3-Lock Defense Architecture combining Computer Vision Liveness, Geo-Velocity Checks, and Spoken Tamil Keypad Voice Calls.

---

## 🚀 Deployment Options

### Option 1: Instant Vercel Deployment (Production Web App) ⚡
This project is configured for **1-click Vercel deployment** with zero deployment errors:
1. Push this folder to a GitHub repository.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"** -> **"Import"** your repository.
3. Keep default settings (Framework: *Other*, Build command: *None*, Output directory: *None*).
4. Click **"Deploy"**!
5. Your live app is instantly online with full live webcam bio-scanner, Tamil voice IVR simulation, and 3-lock consensus receipts.

> **Why Streamlit gave an error on Vercel:**  
> Vercel is a serverless platform with execution timeouts and no persistent WebSocket daemon support. Standard `streamlit run` requires long-running background server processes and bloated C++ binaries (`opencv-python`), causing Vercel builds to time out or exceed package limits. This project resolves that by providing a high-performance web application (`index.html`, `static/`, `vercel.json`, `api/index.py`) that deploys natively on Vercel.

---

### Option 2: Running Streamlit Locally
To run the interactive Streamlit version locally on your machine:
```bash
pip install -r requirements-streamlit.txt
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

### Option 3: Streamlit Community Cloud (Free Hosting for Streamlit)
If you wish to deploy the pure Streamlit version (`app.py`):
1. Push to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Select your repo and set main file to `app.py`.
4. Streamlit Cloud provides persistent WebSocket instances specifically built for Streamlit!

---

## 🔒 The 3-Lock Security Architecture

| Security Lock | Mechanism | Technology | Result |
| :--- | :--- | :--- | :--- |
| **Lock 1: Alive Lock** | Examines blood perfusion, skin chrominance (YCrCb/HSV), and micro-texture gradients | OpenCV, NumPy, Vision AI | **PASS:** Real Living Skin<br/>**FAIL:** Silicone / Tape / Paper Printout |
| **Lock 2: Place Lock** | Calculates Haversine distance and travel speed between deed city and kiosk | Haversine Formula, Python | **PASS:** Feasible Travel (<120 km/h)<br/>**FAIL:** Impossible Speed (e.g. 1320 km/h) |
| **Lock 3: Owner Lock** | Triggers an automated spoken Tamil voice call to the owner's basic 2G phone | gTTS (Tamil), Keypad IVR | **PASS:** Owner presses `1`<br/>**FAIL:** Owner presses `9` or unanswered |

---

## 🎯 How to Demo to Evaluators & Judges

### Scenario A: Real Beneficiary (Legitimate Cash Release — GREEN)
1. In the sidebar, select **Ramasamy M (Trichy)**.
2. Set Kiosk City to **Trichy** (Local transaction).
3. Under **Lock 1**, select **"1. Living Human Skin (Genuine Finger)"** (or point your real finger to the webcam).  
   👉 *Alive Lock shows: `✔ PASS: Real Finger - Verified`*.
4. Under **Lock 2**, distance is `0.0 km`.  
   👉 *Place Lock shows: `✔ PASS: Verified Local Transaction`*.
5. Under **Lock 3**, click the audio player to play the Tamil voice prompt, then press **`[ 1 ] ஆம் (Approve)`** on the keypad.  
   👉 *Owner Lock shows: `✔ PASS: Key [1] Approved`*.
6. Click **"🚀 EXECUTE AEPS CASH WITHDRAWAL TRANSACTION"**.  
   👉 **Outcome:** Balloons celebrate, and a glowing green **"CASH DISPENSED: ₹3,000"** digital receipt is generated!

---

### Scenario B: Scammer Clone Attack (Fraud Thwarted — RED)
1. In the sidebar, keep **Ramasamy M (Trichy)** as the victim.
2. Change the Kiosk City to **Coimbatore** (220 km away), and set elapsed time to **10 minutes**.
3. Under **Lock 1**, select **"2. Cloned Silicone Rubber (Dummy Finger)"** or **"3. Paper Deed Printout"**.  
   👉 *Alive Lock fails: `✖ FAIL: Fraud Detected: Spoofed Presentation Attack`*.
4. Under **Lock 2**, the speed spikes to `1,155 km/h`!  
   👉 *Place Lock fails: `✖ FAIL: Fraud Alert: Impossible Travel Velocity`*.
5. Under **Lock 3**, on the keypad phone, press **`[ 9 ] இல்லை (Scam)`**.  
   👉 *Owner Lock flags: `✖ FAIL: Owner Pressed 9 (Reject)`*.
6. Click **"🚀 EXECUTE AEPS CASH WITHDRAWAL TRANSACTION"**.  
   👉 **Outcome:** Flashing red alert: **"TRANSACTION BLOCKED: FRAUD PREVENTED"**, emergency SMS alert text is dispatched, and the incident is recorded in `data/fraud_logs.csv`!

---

## 📁 Project Directory Layout

```
clonEnd/
├── index.html                 # Vercel entrypoint: Web Terminal
├── vercel.json                # Vercel deployment & routing config
├── .vercelignore              # Deployment ignore rules
├── api/
│   └── index.py               # Vercel Serverless API (Zero-dependency)
├── core/
│   ├── alive_lock.py          # Lock 1: Bio-liveness and presentation attack detector
│   ├── place_lock.py          # Lock 2: Haversine distance and impossible speed check
│   ├── owner_lock.py          # Lock 3: Tamil voice prompt generator & IVR simulator
│   └── decision_engine.py    # Master 3-lock consensus rule engine & audit logger
├── data/
│   ├── beneficiaries.csv      # Sample rural accounts (Farmers, Pensioners, Villagers)
│   ├── fraud_logs.csv         # Permanent audit trail of intercepted attacks
│   └── tamil_nadu_cities.json # Coordinates for Tamil Nadu towns and districts
├── assets/
│   ├── audio/                 # Pre-generated Tamil IVR audio clips (.mp3)
│   └── samples/               # Sample test images for 1-click fail-safe demo
├── static/
│   ├── style.css              # Custom Bank Mitra banking theme styling
│   └── app.js                 # Frontend interactive logic & 3-lock pipeline
├── app.py                     # Streamlit application (for local/Streamlit Cloud)
├── requirements.txt           # Vercel-optimized lightweight requirements
├── requirements-streamlit.txt # Full dependencies for local Streamlit
└── test_core.py               # Automated test suite
```

---

## 💡 Key Viva / Presentation Questions & Answers

1. **Q: Why can't UIDAI's existing mAadhaar biometric lock solve this?**  
   *A:* mAadhaar requires a smartphone and digital literacy. Over 70% of rural AePS beneficiaries are elderly pensioners or manual laborers who only own basic ₹1,000 keypad phones or no phone at all.

2. **Q: Why does the optical reader in shops accept silicone fingers?**  
   *A:* Shop scanners are simple optical or capacitive sensors designed to read 2D ridge contrast. They do not analyze biological blood perfusion, skin chrominance, or micro-texture.

3. **Q: How does Lock 3 work if the user has no internet?**  
   *A:* Lock 3 uses standard Telecom IVR voice calls over 2G GSM cellular networks. Any basic phone (Nokia 105, JioBharat) can receive the automated voice call and transmit keypad DTMF tones (pressing 1 or 9) with zero internet required.
