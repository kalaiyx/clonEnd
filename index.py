"""
clonEnd - Vercel Serverless API
Provides REST API endpoints for 3-Lock Biometric Defense Shield
Compatible with Vercel Python Runtime (Zero external pip dependencies required).
"""

from http.server import BaseHTTPRequestHandler
import json
import math
import os
import random
from datetime import datetime
import urllib.parse

# Path to datasets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Fallback Beneficiaries
FALLBACK_BENEFICIARIES = [
    {
        "aadhaar_no": "2345-6789-1011",
        "name": "Ramasamy M",
        "category": "Farmer",
        "home_city": "Trichy",
        "phone_number": "9842154321",
        "bank_name": "State Bank of India",
        "account_balance": 24500,
        "last_active_time": "2026-10-08 09:30:00",
        "last_active_city": "Trichy"
    },
    {
        "aadhaar_no": "3456-7890-1212",
        "name": "Meenakshi Ammal",
        "category": "Pensioner",
        "home_city": "Thanjavur",
        "phone_number": "9789123456",
        "bank_name": "Canara Bank",
        "account_balance": 14200,
        "last_active_time": "2026-10-08 08:45:00",
        "last_active_city": "Thanjavur"
    },
    {
        "aadhaar_no": "4567-8901-2323",
        "name": "Selvaraj K",
        "category": "Daily Wage Laborer",
        "home_city": "Salem",
        "phone_number": "9443678901",
        "bank_name": "Indian Overseas Bank",
        "account_balance": 8900,
        "last_active_time": "2026-10-08 10:15:00",
        "last_active_city": "Salem"
    },
    {
        "aadhaar_no": "5678-9012-3434",
        "name": "Muthulakshmi R",
        "category": "MGNREGS Worker",
        "home_city": "Madurai",
        "phone_number": "9944512345",
        "bank_name": "Tamilnad Mercantile Bank",
        "account_balance": 11800,
        "last_active_time": "2026-10-08 07:20:00",
        "last_active_city": "Madurai"
    },
    {
        "aadhaar_no": "6789-0123-4545",
        "name": "Arumugam P",
        "category": "Elderly Artisan",
        "home_city": "Dindigul",
        "phone_number": "9865432109",
        "bank_name": "Indian Bank",
        "account_balance": 19400,
        "last_active_time": "2026-10-08 09:00:00",
        "last_active_city": "Dindigul"
    }
]

# Fallback Cities
FALLBACK_CITIES = {
    "Trichy": {"lat": 10.7905, "lon": 78.7047, "district": "Tiruchirappalli"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "district": "Coimbatore"},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "district": "Madurai"},
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378, "district": "Thanjavur"},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "district": "Salem"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "district": "Chennai"},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "district": "Tirunelveli"},
    "Erode": {"lat": 11.3410, "lon": 77.7172, "district": "Erode"},
    "Dindigul": {"lat": 10.3673, "lon": 77.9803, "district": "Dindigul"},
    "Ariyalur": {"lat": 11.1401, "lon": 79.0786, "district": "Ariyalur"},
    "Nagapattinam": {"lat": 10.7672, "lon": 79.8449, "district": "Nagapattinam"},
    "Kumbakonam": {"lat": 10.9602, "lon": 79.3845, "district": "Thanjavur"},
    "Pudukkottai": {"lat": 10.3797, "lon": 78.8208, "district": "Pudukkottai"},
    "Karur": {"lat": 10.9601, "lon": 78.0766, "district": "Karur"},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "district": "Vellore"}
}


def load_cities():
    cities_path = os.path.join(DATA_DIR, "tamil_nadu_cities.json")
    if os.path.exists(cities_path):
        try:
            with open(cities_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return FALLBACK_CITIES


def load_beneficiaries():
    beneficiaries_path = os.path.join(DATA_DIR, "beneficiaries.csv")
    if os.path.exists(beneficiaries_path):
        try:
            rows = []
            with open(beneficiaries_path, "r", encoding="utf-8") as f:
                header = None
                for line in f:
                    parts = [p.strip() for p in line.split(",")]
                    if not header:
                        header = parts
                    elif len(parts) >= len(header):
                        row = dict(zip(header, parts))
                        if "account_balance" in row:
                            row["account_balance"] = int(row["account_balance"])
                        rows.append(row)
            if rows:
                return rows
        except Exception:
            pass
    return FALLBACK_BENEFICIARIES


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_place_lock(home_city: str, kiosk_city: str, elapsed_minutes: int, max_speed_kmh: float = 120.0):
    cities = load_cities()
    c1 = cities.get(home_city, {"lat": 10.7905, "lon": 78.7047})
    c2 = cities.get(kiosk_city, {"lat": 11.0168, "lon": 76.9558})
    
    dist_km = haversine_distance(c1["lat"], c1["lon"], c2["lat"], c2["lon"])
    
    if home_city.strip().lower() == kiosk_city.strip().lower() or dist_km < 15.0:
        return {
            "is_valid": True,
            "distance_km": dist_km,
            "elapsed_minutes": elapsed_minutes,
            "speed_kmh": 0.0,
            "max_speed_kmh": max_speed_kmh,
            "verdict": "Verified Local Transaction",
            "risk_level": "LOW",
            "status_color": "green",
            "home_city": home_city,
            "kiosk_city": kiosk_city,
            "details": f"Transaction initiated within registered home vicinity ({dist_km:.1f} km). Normal customer activity."
        }
    
    hours_elapsed = max(elapsed_minutes / 60.0, 0.0167)
    implied_speed = round(dist_km / hours_elapsed, 1)
    
    if implied_speed > max_speed_kmh:
        return {
            "is_valid": False,
            "distance_km": dist_km,
            "elapsed_minutes": elapsed_minutes,
            "speed_kmh": implied_speed,
            "max_speed_kmh": max_speed_kmh,
            "verdict": "Fraud Alert: Impossible Travel Velocity",
            "risk_level": "CRITICAL",
            "status_color": "red",
            "home_city": home_city,
            "kiosk_city": kiosk_city,
            "details": f"Cloned print attack suspected! Distance between registered location ({home_city}) and Micro-ATM ({kiosk_city}) is {dist_km:.1f} km. Attempted in {elapsed_minutes} mins requires impossible travel speed of {implied_speed:.1f} km/h (Limit: {max_speed_kmh} km/h)."
        }
    else:
        return {
            "is_valid": True,
            "distance_km": dist_km,
            "elapsed_minutes": elapsed_minutes,
            "speed_kmh": implied_speed,
            "max_speed_kmh": max_speed_kmh,
            "verdict": "Verified Regional Travel",
            "risk_level": "MODERATE",
            "status_color": "green",
            "home_city": home_city,
            "kiosk_city": kiosk_city,
            "details": f"Travel velocity plausible. Distance {dist_km:.1f} km in {elapsed_minutes} mins gives speed of {implied_speed:.1f} km/h."
        }


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path in ["/api", "/api/health", ""]:
            self._send_json(200, {
                "status": "online",
                "service": "clonEnd Vercel Serverless Defense API",
                "version": "1.0.0",
                "message": "3-Lock Biometric Defense Shield Active & Operational",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        elif path == "/api/beneficiaries":
            self._send_json(200, {
                "status": "success",
                "count": len(load_beneficiaries()),
                "beneficiaries": load_beneficiaries()
            })
        elif path == "/api/cities":
            self._send_json(200, {
                "status": "success",
                "cities": load_cities()
            })
        elif path == "/api/fraud-logs":
            logs_path = os.path.join(DATA_DIR, "fraud_logs.csv")
            logs = []
            if os.path.exists(logs_path):
                try:
                    with open(logs_path, "r", encoding="utf-8") as f:
                        header = None
                        for line in f:
                            parts = [p.strip() for p in line.split(",")]
                            if not header:
                                header = parts
                            elif len(parts) >= len(header):
                                logs.append(dict(zip(header, parts)))
                except Exception:
                    pass
            self._send_json(200, {
                "status": "success",
                "count": len(logs),
                "logs": logs
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            req_data = {}

        if path == "/api/verify-location":
            home_city = req_data.get("home_city", "Trichy")
            kiosk_city = req_data.get("kiosk_city", "Coimbatore")
            elapsed = int(req_data.get("elapsed_minutes", 10))
            max_spd = float(req_data.get("max_speed_kmh", 120.0))
            res = calculate_place_lock(home_city, kiosk_city, elapsed, max_spd)
            self._send_json(200, res)

        elif path == "/api/verify-ivr":
            dtmf = req_data.get("dtmf_key", "1")
            if dtmf == "1":
                self._send_json(200, {
                    "is_confirmed": True,
                    "status": "APPROVED",
                    "verdict": "Owner Confirmed via Tamil Voice Call",
                    "status_color": "green",
                    "dtmf_key": "1",
                    "details": "Customer pressed '1' on phone keypad. Authorized legitimate cash withdrawal."
                })
            elif dtmf == "9":
                self._send_json(200, {
                    "is_confirmed": False,
                    "status": "REJECTED_BY_OWNER",
                    "verdict": "Fraud Reported: Owner Pressed 9 (Reject)",
                    "status_color": "red",
                    "dtmf_key": "9",
                    "details": "Victim answered keypad call and pressed '9' (Unauthorized). Scam immediately averted!"
                })
            else:
                self._send_json(200, {
                    "is_confirmed": False,
                    "status": "TIMEOUT",
                    "verdict": "Fraud Alert: Voice Call Unanswered / Timeout",
                    "status_color": "red",
                    "dtmf_key": "None",
                    "details": "Registered phone did not answer the IVR call within the 30-second security window."
                })

        elif path == "/api/execute-transaction":
            beneficiary = req_data.get("beneficiary", {})
            kiosk_city = req_data.get("kiosk_city", "Coimbatore")
            amount = int(req_data.get("amount", 3000))
            lock1 = req_data.get("lock1_result", {})
            lock2 = req_data.get("lock2_result", {})
            lock3 = req_data.get("lock3_result", {})

            l1_pass = lock1.get("is_live", False)
            l2_pass = lock2.get("is_valid", False)
            l3_pass = lock3.get("is_confirmed", False)

            all_passed = l1_pass and l2_pass and l3_pass
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            txn_id = f"AEPS-{datetime.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}"

            if all_passed:
                cur_bal = int(beneficiary.get("account_balance", 20000))
                new_bal = max(0, cur_bal - amount)
                self._send_json(200, {
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
                })
            else:
                failed_locks = []
                if not l1_pass:
                    failed_locks.append(f"Lock 1 (Alive Lock: {lock1.get('verdict', 'Liveness Failed')})")
                if not l2_pass:
                    failed_locks.append(f"Lock 2 (Place Lock: {lock2.get('verdict', 'Travel Anomaly')})")
                if not l3_pass:
                    failed_locks.append(f"Lock 3 (Owner Lock: {lock3.get('verdict', 'Owner Unverified')})")

                failed_summary = " + ".join([fl.split('(')[1].split(':')[0] for fl in failed_locks])
                detailed_reason = f"Breach detected: {', '.join(failed_locks)}"
                sms_alert_text = (
                    f"🚨 எச்சரிக்கை (FRAUD ALERT)! உங்கள் ஆதார் எண் {beneficiary.get('aadhaar_no')} "
                    f"பயன்படுத்தி {kiosk_city}-ல் ₹{amount} திருடப்பட்ட முயற்சி clonEnd-ஆல் "
                    f"வெற்றிகரமாக தடுக்கப்பட்டது. காரணம்: {failed_summary}."
                )

                self._send_json(200, {
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
                })
        else:
            self._send_json(404, {"error": "Endpoint not found"})
