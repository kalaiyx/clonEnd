"""
clonEnd - Decision Engine
Master 3-Lock Convergence Logic & Audit Logging

Convergence Rule:
- All 3 Locks PASS -> Cash Released (Green)
- Any Lock FAILS -> Cash BLOCKED, Incident Logged to CSV, Emergency Alert Triggered (Red)
"""

import os
import csv
import random
from datetime import datetime
from typing import Dict, Any, List


class DecisionEngine:
    def __init__(self, fraud_logs_path: str = None):
        if fraud_logs_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fraud_logs_path = os.path.join(base_dir, "data", "fraud_logs.csv")
        self.fraud_logs_path = fraud_logs_path

    def evaluate_transaction(self,
                             beneficiary: Dict[str, Any],
                             kiosk_city: str,
                             amount: int,
                             alive_result: Dict[str, Any],
                             place_result: Dict[str, Any],
                             owner_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates the 3 locks and makes the final go / no-go decision.
        """
        lock1_pass = alive_result.get("is_live", False)
        lock2_pass = place_result.get("is_valid", False)
        lock3_pass = owner_result.get("is_confirmed", False)

        all_passed = lock1_pass and lock2_pass and lock3_pass
        failed_locks = []

        if not lock1_pass:
            failed_locks.append(f"Lock 1 (Alive Lock: {alive_result.get('verdict', 'Liveness Failed')})")
        if not lock2_pass:
            failed_locks.append(f"Lock 2 (Place Lock: {place_result.get('verdict', 'Travel Anomaly')})")
        if not lock3_pass:
            failed_locks.append(f"Lock 3 (Owner Lock: {owner_result.get('verdict', 'Owner Unverified')})")

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txn_id = f"AEPS-{datetime.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}"

        if all_passed:
            # CASH DISPENSED
            current_bal = int(beneficiary.get("account_balance", 20000))
            new_bal = max(0, current_bal - amount)
            return {
                "decision": "APPROVED",
                "status_title": "CASH DISPENSED: TRANSACTION RELEASED",
                "status_color": "green",
                "txn_id": txn_id,
                "timestamp": now_str,
                "amount": amount,
                "new_balance": new_bal,
                "beneficiary_name": beneficiary.get("name"),
                "aadhaar_no": beneficiary.get("aadhaar_no"),
                "bank_name": beneficiary.get("bank_name"),
                "kiosk_city": kiosk_city,
                "summary": "All 3 security locks passed successfully. Legitimate biometric withdrawal authenticated."
            }
        else:
            # FRAUD DETECTED & BLOCKED
            failed_summary = " + ".join([fl.split('(')[1].split(':')[0] for fl in failed_locks])
            details_list = []
            if not lock1_pass:
                details_list.append(f"PAD: {alive_result.get('fraud_type')} [Score {alive_result.get('liveness_score')}%]")
            if not lock2_pass:
                details_list.append(f"Geo: {place_result.get('details')}")
            if not lock3_pass:
                details_list.append(f"Voice: {owner_result.get('details')}")
            detailed_reason = "; ".join(details_list)

            # Log incident to CSV
            self._log_fraud_attempt(
                timestamp=now_str,
                aadhaar_no=beneficiary.get("aadhaar_no", "UNKNOWN"),
                name=beneficiary.get("name", "Unknown"),
                kiosk_city=kiosk_city,
                amount=amount,
                failed_locks=failed_summary,
                details=detailed_reason,
                action="BLOCKED & SMS Dispatched"
            )

            sms_alert_text = (
                f"🚨 எச்சரிக்கை (FRAUD ALERT)! உங்கள் ஆதார் எண் {beneficiary.get('aadhaar_no')} "
                f"பயன்படுத்தி {kiosk_city}-ல் ₹{amount} திருடப்பட்ட முயற்சி clonEnd-ஆல் "
                f"வெற்றிகரமாக தடுக்கப்பட்டது. காரணம்: {failed_summary}."
            )

            return {
                "decision": "BLOCKED",
                "status_title": "TRANSACTION BLOCKED: FRAUD PREVENTED",
                "status_color": "red",
                "txn_id": txn_id,
                "timestamp": now_str,
                "amount": amount,
                "beneficiary_name": beneficiary.get("name"),
                "aadhaar_no": beneficiary.get("aadhaar_no"),
                "kiosk_city": kiosk_city,
                "failed_locks": failed_locks,
                "detailed_reason": detailed_reason,
                "sms_alert": sms_alert_text,
                "summary": "Biometric clone scam thwarted! One or more security locks failed."
            }

    def _log_fraud_attempt(self, timestamp: str, aadhaar_no: str, name: str,
                           kiosk_city: str, amount: int, failed_locks: str,
                           details: str, action: str):
        """
        Appends blocked fraud attempt into the fraud logs audit file.
        """
        file_exists = os.path.exists(self.fraud_logs_path)
        try:
            with open(self.fraud_logs_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["timestamp", "aadhaar_no", "beneficiary_name",
                                     "attempted_city", "amount_requested",
                                     "failed_locks", "details", "action_taken"])
                writer.writerow([timestamp, aadhaar_no, name, kiosk_city, amount,
                                 failed_locks, details, action])
        except Exception as e:
            print(f"Error logging fraud attempt: {e}")
