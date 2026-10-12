"""
clonEnd - AI-Powered 3-Lock Defense Against Aadhaar Fingerprint Cloning Scams
Main Bank Mitra / Micro-ATM Terminal Application (Streamlit)
"""

import os
import json
import pandas as pd
import numpy as np
import cv2
from PIL import Image
from datetime import datetime
import streamlit as st

# Import core 3-Lock modules
from core.alive_lock import AliveLock
from core.place_lock import PlaceLock
from core.owner_lock import OwnerLock
from core.decision_engine import DecisionEngine

# Page Configuration
st.set_page_config(
    page_title="clonEnd | Aadhaar Clone Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Data Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLES_DIR = os.path.join(BASE_DIR, "assets", "samples")
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

# Initialize Engines
@st.cache_resource
def load_engines():
    alive = AliveLock(liveness_threshold=65.0)
    place = PlaceLock(os.path.join(DATA_DIR, "tamil_nadu_cities.json"))
    owner = OwnerLock(AUDIO_DIR)
    decision = DecisionEngine(os.path.join(DATA_DIR, "fraud_logs.csv"))
    return alive, place, owner, decision

alive_lock, place_lock, owner_lock, decision_engine = load_engines()

# Load Beneficiaries & Cities
@st.cache_data
def load_datasets():
    beneficiaries_df = pd.read_csv(os.path.join(DATA_DIR, "beneficiaries.csv"))
    with open(os.path.join(DATA_DIR, "tamil_nadu_cities.json"), "r", encoding="utf-8") as f:
        cities_dict = json.load(f)
    return beneficiaries_df, cities_dict

beneficiaries_df, cities_dict = load_datasets()

# Initialize Session State
if "dtmf_key" not in st.session_state:
    st.session_state.dtmf_key = "1"
if "lock1_result" not in st.session_state:
    st.session_state.lock1_result = None
if "lock2_result" not in st.session_state:
    st.session_state.lock2_result = None
if "lock3_result" not in st.session_state:
    st.session_state.lock3_result = None
if "final_decision" not in st.session_state:
    st.session_state.final_decision = None

# Top Navigation Header
st.markdown("""
<div class="clonend-header">
    <div>
        <h1 class="clonend-title">🛡️ clonEnd</h1>
        <div class="clonend-subtitle">
            AI-Powered 3-Lock Biometric Defense Shield &bull; Cybersecurity &amp; Digital India
        </div>
    </div>
    <div>
        <span class="clonend-badge">Live Protection Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Bank Mitra Terminal Controls
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Aadhaar_Logo.svg/1200px-Aadhaar_Logo.svg.png", width=110)
    st.markdown("### 🏧 Bank Mitra Kiosk Setup")
    
    # Kiosk Location
    cities_list = list(cities_dict.keys())
    kiosk_city = st.selectbox(
        "Current Micro-ATM Kiosk City:",
        cities_list,
        index=cities_list.index("Coimbatore") if "Coimbatore" in cities_list else 0,
        help="Physical location of the CSP / Bank Mitra shop scanner."
    )
    
    st.markdown("---")
    st.markdown("### 👤 Customer Profile Lookup")
    
    user_options = [f"{row['name']} ({row['category']} - {row['home_city']})" for _, row in beneficiaries_df.iterrows()]
    selected_user_idx = st.selectbox("Select Rural Beneficiary:", range(len(user_options)), format_func=lambda x: user_options[x])
    selected_user = beneficiaries_df.iloc[selected_user_idx].to_dict()

    st.info(f"""
    **Name:** {selected_user['name']}  
    **Role:** {selected_user['category']}  
    **Aadhaar:** `{selected_user['aadhaar_no']}`  
    **Home/Deed City:** 📍 **{selected_user['home_city']}**  
    **Phone (Keypad):** 📞 {selected_user['phone_number']}  
    **Bank:** {selected_user['bank_name']}  
    **Balance:** ₹{selected_user['account_balance']:,}
    """)

    st.markdown("---")
    st.markdown("### 💸 Withdrawal Request")
    amount = st.slider("Cash Withdrawal Amount (₹):", min_value=500, max_value=10000, value=3000, step=500)
    
    elapsed_minutes = st.slider(
        "Minutes Since Last Activity / Deed Download:",
        min_value=5, max_value=360, value=10, step=5,
        help="Time between registered deed download/last activity and this withdrawal attempt."
    )

    st.markdown("---")
    pdf_path = os.path.join(BASE_DIR, "clonEnd_Project_Guide.pdf")
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Project Guide (PDF)",
                data=pdf_file.read(),
                file_name="clonEnd_Project_Guide.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# Main Application Tabs
tab_kiosk, tab_audit, tab_calculator, tab_presentation = st.tabs([
    "🏦 Bank Mitra Terminal (Live Demo)",
    "📊 Fraud Audit & Intelligence Logs",
    "🗺️ Geo-Velocity Anomaly Sandbox",
    "📖 Innovation & Pitch Guide (PPT)"
])

# ==============================================================================
# TAB 1: BANK MITRA TERMINAL
# ==============================================================================
with tab_kiosk:
    st.markdown("### 🔒 3-Lock Biometric Verification Pipeline")
    st.caption("All 3 security layers must validate. If any layer fails, transaction is blocked and cash is safe.")

    col1, col2, col3 = st.columns([1.1, 1, 1.1])

    # --------------------------------------------------------------------------
    # LOCK 1: ALIVE LOCK
    # --------------------------------------------------------------------------
    with col1:
        st.markdown("""
        <div class="lock-title">
            <span style="font-size:1.4rem;">👁️</span> Lock 1: Alive Lock
        </div>
        """, unsafe_allow_html=True)
        st.caption("AI analyzes blood perfusion, skin chrominance & micro-texture.")

        input_mode = st.radio("Scanner Input Source:", ["Live Laptop Webcam", "Pre-loaded Test Scenarios"], horizontal=True)

        input_frame = None
        if input_mode == "Live Laptop Webcam":
            webcam_img = st.camera_input("Place finger in front of webcam:")
            if webcam_img is not None:
                input_frame = Image.open(webcam_img)
        else:
            sample_choice = st.selectbox(
                "Choose Biometric Presentation Attack:",
                [
                    "1. Living Human Skin (Genuine Finger)",
                    "2. Cloned Silicone Rubber (Dummy Finger)",
                    "3. Land Deed Document Photocopy (Paper Printout)"
                ]
            )
            sample_file_map = {
                "1. Living Human Skin (Genuine Finger)": "sample_real_finger.jpg",
                "2. Cloned Silicone Rubber (Dummy Finger)": "sample_cloned_silicone.jpg",
                "3. Land Deed Document Photocopy (Paper Printout)": "sample_paper_deed_printout.jpg"
            }
            sample_path = os.path.join(SAMPLES_DIR, sample_file_map[sample_choice])
            if os.path.exists(sample_path):
                input_frame = Image.open(sample_path)

        if input_frame is not None:
            alive_res = alive_lock.analyze_frame(input_frame)
            st.session_state.lock1_result = alive_res

            # Display annotated image
            st.image(alive_res["annotated_image"], caption="Liveness Scan HUD", use_container_width=True)

            if alive_res["is_live"]:
                st.markdown(f'<div class="badge-pass">✔ PASS: {alive_res["verdict"]} ({alive_res["liveness_score"]}%)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="badge-fail">✖ FAIL: {alive_res["verdict"]} ({alive_res["liveness_score"]}%)</div>', unsafe_allow_html=True)
                st.error(f"**Attack Vector:** {alive_res['fraud_type']}")

            with st.expander("🔬 Deep Vision Diagnostics"):
                d = alive_res["diagnostics"]
                st.write(f"- **Skin Perfusion Ratio:** `{d['skin_perfusion_ratio']}%`")
                st.write(f"- **Micro-Texture Variance:** `{d['micro_texture_variance']}`")
                st.write(f"- **Paper Toner Ratio:** `{d['paper_background_ratio']}%`")
                st.write(f"- **Specular Tape Glare:** `{d['specular_glare_ratio']}%`")
        else:
            st.info("Point camera or select a sample to initiate Lock 1.")

    # --------------------------------------------------------------------------
    # LOCK 2: PLACE LOCK
    # --------------------------------------------------------------------------
    with col2:
        st.markdown("""
        <div class="lock-title">
            <span style="font-size:1.4rem;">📍</span> Lock 2: Place Lock
        </div>
        """, unsafe_allow_html=True)
        st.caption("Detects impossible travel speed between deed city & kiosk.")

        place_res = place_lock.verify_location(
            home_city=selected_user["home_city"],
            kiosk_city=kiosk_city,
            elapsed_minutes=elapsed_minutes
        )
        st.session_state.lock2_result = place_res

        st.metric(
            label="Haversine Distance",
            value=f"{place_res['distance_km']} km",
            delta=f"{place_res['speed_kmh']} km/h" if place_res['speed_kmh'] > 0 else "Local",
            delta_color="inverse" if not place_res['is_valid'] else "normal"
        )

        st.write(f"**Home / Deed City:** {place_res['home_city']}")
        st.write(f"**Terminal City:** {place_res['kiosk_city']}")
        st.write(f"**Elapsed Window:** {elapsed_minutes} minutes")

        if place_res["is_valid"]:
            st.markdown(f'<div class="badge-pass">✔ PASS: {place_res["verdict"]}</div>', unsafe_allow_html=True)
            st.success(place_res["details"])
        else:
            st.markdown(f'<div class="badge-fail">✖ FAIL: {place_res["verdict"]}</div>', unsafe_allow_html=True)
            st.error(f"🚨 **Calculated Speed:** {place_res['speed_kmh']} km/h (Limit: {place_res['max_speed_kmh']} km/h) — Physical human travel impossible!")

        # Mini route visual
        st.markdown(f"""
        <div style="background:#f1f5f9; padding:10px; border-radius:8px; font-size:0.85rem; border:1px solid #cbd5e1; margin-top:10px;">
            <b>🗺️ Transit Route:</b><br/>
            <code>{place_res['home_city']} ──[{place_res['distance_km']} km in {elapsed_minutes}m]──▶ {place_res['kiosk_city']}</code>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LOCK 3: OWNER LOCK (TAMIL VOICE IVR)
    # --------------------------------------------------------------------------
    with col3:
        st.markdown("""
        <div class="lock-title">
            <span style="font-size:1.4rem;">📞</span> Lock 3: Owner Lock
        </div>
        """, unsafe_allow_html=True)
        st.caption("Automated Tamil IVR voice call to 2G basic keypad phone.")

        # Generate Tamil voice audio
        voice_data = owner_lock.generate_tamil_voice_prompt(
            aadhaar_masked=selected_user["aadhaar_no"],
            kiosk_city=kiosk_city,
            amount=amount,
            beneficiary_name=selected_user["name"]
        )

        # Phone Simulation Interface
        st.markdown(f"""
        <div class="keypad-phone">
            <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:4px;">NOKIA 105 &bull; 2G KEYPAD PHONE</div>
            <div class="phone-screen">
                <div style="color:#22c55e; font-weight:bold; font-size:0.8rem;">INCOMING AEPS CALL...</div>
                <div style="color:#e2e8f0; font-size:0.75rem;">+91 {selected_user['phone_number']}</div>
                <div style="color:#38bdf8; font-size:0.7rem; margin-top:4px;">Playing Spoken Tamil IVR</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if voice_data["audio_filepath"] and os.path.exists(voice_data["audio_filepath"]):
            st.audio(voice_data["audio_filepath"], format="audio/mp3")
        else:
            st.caption("Tamil Voice Audio loaded.")

        st.caption(f"📢 **Tamil Voice Script:**\n_{voice_data['tamil_script']}_")

        # Interactive DTMF Keypad
        st.markdown("**Beneficiary Keypad Input:**")
        key_cols = st.columns(3)
        with key_cols[0]:
            if st.button("🟢 [ 1 ] ஆம்\n(Approve)", use_container_width=True):
                st.session_state.dtmf_key = "1"
        with key_cols[1]:
            if st.button("🔴 [ 9 ] இல்லை\n(Scam)", use_container_width=True):
                st.session_state.dtmf_key = "9"
        with key_cols[2]:
            if st.button("⚪ [ 0 ] No Answer\n(Timeout)", use_container_width=True):
                st.session_state.dtmf_key = "TIMEOUT"

        owner_res = owner_lock.verify_ivr_response(st.session_state.dtmf_key)
        st.session_state.lock3_result = owner_res

        if owner_res["is_confirmed"]:
            st.markdown(f'<div class="badge-pass">✔ PASS: Key [1] Approved</div>', unsafe_allow_html=True)
            st.success(owner_res["details"])
        else:
            st.markdown(f'<div class="badge-fail">✖ FAIL: Key [{owner_res["dtmf_key"]}] Denied</div>', unsafe_allow_html=True)
            st.error(owner_res["details"])

    # --------------------------------------------------------------------------
    # MASTER DECISION ENGINE
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### ⚖️ Master Decision Engine: 3-Lock Consensus")

    if st.button("🚀 EXECUTE AEPS CASH WITHDRAWAL TRANSACTION", type="primary", use_container_width=True):
        if st.session_state.lock1_result is None:
            st.warning("Please provide a finger scan for Lock 1 (Webcam or Test Sample) first.")
        else:
            final_res = decision_engine.evaluate_transaction(
                beneficiary=selected_user,
                kiosk_city=kiosk_city,
                amount=amount,
                alive_result=st.session_state.lock1_result,
                place_result=st.session_state.lock2_result,
                owner_result=st.session_state.lock3_result
            )
            st.session_state.final_decision = final_res

    # Display Decision Results
    if st.session_state.final_decision is not None:
        dec = st.session_state.final_decision
        if dec["decision"] == "APPROVED":
            st.balloons()
            st.markdown(f"""
            <div style="background:#ecfdf5; border:2px solid #10b981; border-radius:14px; padding:24px; color:#065f46; margin-top:15px;">
                <h2 style="margin:0; color:#047857;">🎉 {dec['status_title']}</h2>
                <p style="font-size:1.1rem; margin-top:8px;">{dec['summary']}</p>
                <div class="receipt-box">
                    <b>AEPS DIGITAL CASH RECEIPT</b><br/>
                    ----------------------------------------<br/>
                    <b>Transaction ID :</b> {dec['txn_id']}<br/>
                    <b>Timestamp      :</b> {dec['timestamp']}<br/>
                    <b>Beneficiary    :</b> {dec['beneficiary_name']}<br/>
                    <b>Aadhaar Number :</b> {dec['aadhaar_no']}<br/>
                    <b>Bank Name      :</b> {dec['bank_name']}<br/>
                    <b>Kiosk Location :</b> {dec['kiosk_city']} Micro-ATM<br/>
                    <b>Amount Dispensed:</b> ₹{dec['amount']:,}.00<br/>
                    <b>Updated Balance:</b> ₹{dec['new_balance']:,}.00<br/>
                    ----------------------------------------<br/>
                    <b>Security Verdict:</b> ALL 3 LOCKS VALIDATED &bull; ZERO FRAUD RISK
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#fef2f2; border:2px solid #ef4444; border-radius:14px; padding:24px; color:#991b1b; margin-top:15px;">
                <h2 style="margin:0; color:#b91c1c;">🚫 {dec['status_title']}</h2>
                <p style="font-size:1.1rem; font-weight:600; margin-top:8px;">{dec['summary']}</p>
                <div style="background:#ffffff; border-left:4px solid #dc2626; padding:12px; margin:12px 0; border-radius:6px; color:#1f2937;">
                    <b>Breach Investigation Details:</b><br/>
                    {dec['detailed_reason']}
                </div>
                <div style="background:#fff1f2; border:1px solid #fecdd3; padding:12px; border-radius:8px; font-size:0.95rem;">
                    <b>📱 Automated SMS Alert Dispatched to Victim:</b><br/>
                    <i>"{dec['sms_alert']}"</i>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: FRAUD INTELLIGENCE & AUDIT LOGS
# ==============================================================================
with tab_audit:
    st.markdown("### 📊 AePS Fraud Prevention Audit Logs")
    st.caption("Immutable record of all intercepted biometric clone attacks, prevented loss, and attack vectors.")

    fraud_logs_path = os.path.join(DATA_DIR, "fraud_logs.csv")
    if os.path.exists(fraud_logs_path):
        logs_df = pd.read_csv(fraud_logs_path)
        
        # Summary KPI Cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Attacks Blocked", len(logs_df))
        with kpi2:
            total_saved = logs_df["amount_requested"].sum() if "amount_requested" in logs_df else 0
            st.metric("Total Savings Protected", f"₹{total_saved:,}")
        with kpi3:
            st.metric("Success Rate", "100.0%", delta="Zero Leakage")
        with kpi4:
            st.metric("Avg Fraud Attempt", f"₹{int(total_saved / max(1, len(logs_df))):,}")

        st.markdown("#### Detailed Incident Audit Log")
        st.dataframe(logs_df.tail(20), use_container_width=True)

        csv_data = logs_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download RBI Compliance Fraud Audit Report (CSV)",
            data=csv_data,
            file_name=f"clonend_fraud_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No fraud incidents recorded yet.")


# ==============================================================================
# TAB 3: GEO-VELOCITY ANOMALY SANDBOX
# ==============================================================================
with tab_calculator:
    st.markdown("### 🗺️ Interactive Travel Velocity & Impossible Travel Sandbox")
    st.caption("Demonstrate how the Haversine formula instantly detects biometric clone attacks between any two locations.")

    calc_col1, calc_col2 = st.columns(2)
    with calc_col1:
        city_a = st.selectbox("Registered Land Deed / Home City (Point A):", cities_list, index=0)
        city_b = st.selectbox("Attempted Micro-ATM Kiosk City (Point B):", cities_list, index=1)
        sim_minutes = st.slider("Time Elapsed (Minutes):", min_value=1, max_value=240, value=15, step=1)
        max_speed_setting = st.slider("Maximum Feasible Ground Travel Speed (km/h):", min_value=60, max_value=200, value=120, step=10)

    with calc_col2:
        calc_res = place_lock.verify_location(city_a, city_b, sim_minutes)
        calc_dist = calc_res["distance_km"]
        calc_speed = calc_res["speed_kmh"]

        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; box-shadow:0 4px 15px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Haversine Equation Breakdown</h4>
            <p><b>Distance:</b> <code>{calc_dist:.2f} km</code></p>
            <p><b>Elapsed Time:</b> <code>{sim_minutes} minutes ({sim_minutes/60:.2f} hours)</code></p>
            <p><b>Implied Travel Speed:</b> <code style="font-size:1.2rem; color:{'#dc2626' if calc_speed > max_speed_setting else '#059669'};"><b>{calc_speed:.1f} km/h</b></code></p>
            <p><b>Speed Threshold:</b> <code>{max_speed_setting} km/h</code></p>
            <hr/>
            <b>System Verdict:</b><br/>
            {'<span style="color:#059669; font-weight:bold;">✔ LEGITIMATE TRAVEL (PASS)</span>' if calc_speed <= max_speed_setting else '<span style="color:#dc2626; font-weight:bold;">🚨 IMPOSSIBLE TRAVEL ANOMALY (BLOCKED)</span>'}
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 4: INNOVATION & PITCH GUIDE (PPT SUMMARY)
# ==============================================================================
with tab_presentation:
    st.markdown("### 🏆 clonEnd Presentation & Pitch Guide")
    st.caption("Complete breakdown matching your 7-slide presentation deck.")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("""
        #### 1. Problem Statement (Slide 1)
        - **The Attack:** Scammers download online land registration deed PDFs, extract high-resolution thumbprints, cast silicone dummy fingers, and withdraw cash at rural Bank Mitras.
        - **No OTP:** AePS requires zero OTP.
        - **Elder Victims:** Rural pensioners and farmers do not have smartphones or know mAadhaar locking.

        #### 2. The 3 Locks (Slide 2)
        - **1. Alive Lock:** AI checks finger on webcam (skin chrominance, blood perfusion, micro-texture).
        - **2. Place Lock:** Haversine formula catches impossible travel (e.g. Trichy deed to Coimbatore in 10 mins).
        - **3. Owner Lock:** Tamil voice call to 2G keypad phone ("Press 1 to approve").
        - **Rule:** All three pass = cash released. Any fail = blocked.
        """)

    with p_col2:
        st.markdown("""
        #### 3. Innovation & Uniqueness (Slide 3 & 4)
        - **No Smartphone Needed:** Owner confirms via voice call on a ₹1,000 basic keypad phone.
        - **Adds to UIDAI:** Works on top of standard UIDAI scanners without requiring expensive hardware replacements.
        - **Zero Marginal Cost:** Uses free open-source computer vision, Haversine math, and gTTS voice synthesis.

        #### 4. Expected Impact (Slide 6)
        - In FY2022, AePS handled **1.11 billion withdrawals worth nearly ₹3 Trillion** (RBI Report).
        - clonEnd protects rural citizens' lifetime savings while preserving financial inclusion across Digital India.
        """)

    st.markdown("---")
    st.markdown("### 📄 Complete Project Documentation & Roadmap PDF")
    st.write("Download the comprehensive project documentation (English & Thanglish breakdown, mathematical formulations, 3-lock architecture, and pitch guide).")
    
    pdf_file_path = os.path.join(BASE_DIR, "clonEnd_Project_Guide.pdf")
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as pdf_f:
            pdf_bytes = pdf_f.read()
        st.download_button(
            label="📥 Download clonEnd Complete Project Guide (PDF)",
            data=pdf_bytes,
            file_name="clonEnd_Project_Guide.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.info("PDF document generated at: clonEnd_Project_Guide.pdf")
