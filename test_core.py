"""
clonEnd Test Suite
Validates AliveLock, PlaceLock, OwnerLock, and DecisionEngine
"""

import cv2
import sys
import io

# Ensure UTF-8 output on Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.alive_lock import AliveLock
from core.place_lock import PlaceLock
from core.owner_lock import OwnerLock
from core.decision_engine import DecisionEngine

def test_system():
    print("=" * 60)
    print("1. TESTING LOCK 1: ALIVE LOCK")
    print("=" * 60)
    alive = AliveLock(liveness_threshold=65.0)
    samples = [
        "sample_real_finger.jpg",
        "sample_cloned_silicone.jpg",
        "sample_paper_deed_printout.jpg"
    ]
    alive_results = {}
    for s in samples:
        img = cv2.imread(f"assets/samples/{s}")
        res = alive.analyze_frame(img)
        alive_results[s] = res
        print(f"[{s}] -> Score: {res['liveness_score']}% | Live: {res['is_live']} | Verdict: {res['verdict']}")

    print("\n" + "=" * 60)
    print("2. TESTING LOCK 2: PLACE LOCK")
    print("=" * 60)
    place = PlaceLock(max_plausible_speed_kmh=120.0)
    
    # Scenario A: Genuine local transaction (Trichy -> Trichy)
    res_local = place.verify_location("Trichy", "Trichy", elapsed_minutes=15)
    print(f"Local Test: {res_local['verdict']} | Valid: {res_local['is_valid']} | Speed: {res_local['speed_kmh']} km/h")

    # Scenario B: Impossible travel attack (Trichy -> Coimbatore, 220 km in 10 mins)
    res_impossible = place.verify_location("Trichy", "Coimbatore", elapsed_minutes=10)
    print(f"Attack Test: {res_impossible['verdict']} | Valid: {res_impossible['is_valid']} | Speed: {res_impossible['speed_kmh']} km/h")

    print("\n" + "=" * 60)
    print("3. TESTING LOCK 3: OWNER LOCK (TAMIL VOICE IVR)")
    print("=" * 60)
    owner = OwnerLock()
    prompt = owner.generate_tamil_voice_prompt(
        aadhaar_masked="XXXX-XXXX-1011",
        kiosk_city="Coimbatore",
        amount=5000,
        beneficiary_name="Ramasamy"
    )
    print(f"Tamil Script:\n{prompt['tamil_script']}")
    if prompt['audio_filepath']:
        print(f"Audio file generated: {prompt['audio_filepath']}")

    res_approve = owner.verify_ivr_response("1")
    res_reject = owner.verify_ivr_response("9")
    print(f"Key 1 -> Confirmed: {res_approve['is_confirmed']} | {res_approve['verdict']}")
    print(f"Key 9 -> Confirmed: {res_reject['is_confirmed']} | {res_reject['verdict']}")

    print("\n" + "=" * 60)
    print("4. TESTING MASTER DECISION ENGINE")
    print("=" * 60)
    engine = DecisionEngine()
    dummy_beneficiary = {
        "aadhaar_no": "2345-6789-1011",
        "name": "Ramasamy M",
        "account_balance": 24500,
        "bank_name": "State Bank of India"
    }

    # Case 1: All 3 pass -> Genuine transaction
    dec_pass = engine.evaluate_transaction(
        beneficiary=dummy_beneficiary,
        kiosk_city="Trichy",
        amount=3000,
        alive_result=alive_results["sample_real_finger.jpg"],
        place_result=res_local,
        owner_result=res_approve
    )
    print(f"[Legitimate Case] Decision: {dec_pass['decision']} | {dec_pass['status_title']}")

    # Case 2: Cloned thumbprint attack (Fake silicone + Impossible travel)
    dec_fail = engine.evaluate_transaction(
        beneficiary=dummy_beneficiary,
        kiosk_city="Coimbatore",
        amount=10000,
        alive_result=alive_results["sample_cloned_silicone.jpg"],
        place_result=res_impossible,
        owner_result=res_reject
    )
    print(f"[Attack Case] Decision: {dec_fail['decision']} | {dec_fail['status_title']}")
    print(f"Failed Locks: {dec_fail.get('failed_locks')}")
    print(f"SMS Alert Dispatched: {dec_fail.get('sms_alert')}")

if __name__ == "__main__":
    test_system()
