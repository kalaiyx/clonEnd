"""
clonEnd - Lock 2: Place Lock
Geo-Location Velocity & Impossible Travel Anomaly Detection

Uses the Haversine spherical distance formula to evaluate geographic travel
velocity between the beneficiary's registered land deed/home location and
the current Bank Mitra Micro-ATM kiosk. Catches cloned prints used far from the owner.
"""

import math
import json
import os
from typing import Dict, Any, Tuple


class PlaceLock:
    def __init__(self, cities_file_path: str = None, max_plausible_speed_kmh: float = 120.0):
        self.max_speed = max_plausible_speed_kmh
        if cities_file_path is None:
            # Default to relative data location
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cities_file_path = os.path.join(base_dir, "data", "tamil_nadu_cities.json")
        
        self.cities = self._load_cities(cities_file_path)

    def _load_cities(self, file_path: str) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates great-circle distance between two GPS coordinates in kilometers.
        """
        R = 6371.0  # Earth's radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    def verify_location(self, home_city: str, kiosk_city: str, elapsed_minutes: int) -> Dict[str, Any]:
        """
        Verifies if travel from home/last city to current kiosk city within elapsed_minutes
        is humanly possible or represents an impossible velocity biometric clone attack.
        """
        # Ensure cities exist in dataset
        if home_city not in self.cities:
            # Fallback if unknown
            lat1, lon1 = 10.7905, 78.7047  # Default Trichy
        else:
            lat1, lon1 = self.cities[home_city]["lat"], self.cities[home_city]["lon"]

        if kiosk_city not in self.cities:
            lat2, lon2 = 11.0168, 76.9558  # Default Coimbatore
        else:
            lat2, lon2 = self.cities[kiosk_city]["lat"], self.cities[kiosk_city]["lon"]

        # 1. Calculate Haversine Distance
        distance_km = self.haversine_distance(lat1, lon1, lat2, lon2)

        # 2. Local proximity check
        if home_city.strip().lower() == kiosk_city.strip().lower() or distance_km < 15.0:
            return {
                "is_valid": True,
                "distance_km": distance_km,
                "elapsed_minutes": elapsed_minutes,
                "speed_kmh": 0.0,
                "max_speed_kmh": self.max_speed,
                "verdict": "Verified Local Transaction",
                "risk_level": "LOW",
                "status_color": "green",
                "home_city": home_city,
                "kiosk_city": kiosk_city,
                "details": f"Transaction initiated within registered home vicinity ({distance_km:.1f} km). Normal customer activity."
            }

        # 3. Calculate Travel Velocity
        hours_elapsed = max(elapsed_minutes / 60.0, 0.0167)  # At least 1 minute
        implied_speed = round(distance_km / hours_elapsed, 1)

        # 4. Check for Impossible Travel Anomaly
        if implied_speed > self.max_speed:
            # Impossible speed detected
            is_valid = False
            verdict = "Fraud Alert: Impossible Travel Velocity"
            risk_level = "CRITICAL"
            status_color = "red"
            details = (
                f"Cloned print attack suspected! Distance between registered location "
                f"({home_city}) and Micro-ATM ({kiosk_city}) is {distance_km:.1f} km. "
                f"Attempted in {elapsed_minutes} mins requires impossible travel speed of "
                f"{implied_speed:.1f} km/h (Limit: {self.max_speed} km/h)."
            )
        else:
            # Feasible travel
            is_valid = True
            verdict = "Verified Regional Travel"
            risk_level = "MODERATE"
            status_color = "green"
            details = (
                f"Travel velocity plausible. Distance {distance_km:.1f} km in "
                f"{elapsed_minutes} mins gives speed of {implied_speed:.1f} km/h."
            )

        return {
            "is_valid": is_valid,
            "distance_km": distance_km,
            "elapsed_minutes": elapsed_minutes,
            "speed_kmh": implied_speed,
            "max_speed_kmh": self.max_speed,
            "verdict": verdict,
            "risk_level": risk_level,
            "status_color": status_color,
            "home_city": home_city,
            "kiosk_city": kiosk_city,
            "details": details,
            "coordinates": {
                "home": {"lat": lat1, "lon": lon1},
                "kiosk": {"lat": lat2, "lon": lon2}
            }
        }
