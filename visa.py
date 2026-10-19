import os
import json
import hmac
import hashlib
import datetime
from pathlib import Path
import random
import keyring

SERVICE_NAME = "FLVX_Borderland_System"
SALT_KEY = "encryption_salt"
CACHE = Path(".flux_core_cache.dat")
MAIN_FILE = Path("visa.txt")
DATE_FILE = Path("dates.txt")
DAYS_FILE = Path("days_valid.txt")
def get_or_create_salt():
    salt = keyring.get_password(SERVICE_NAME, SALT_KEY)
    if not salt:
        salt = os.urandom(32).hex()
        keyring.set_password(SERVICE_NAME, SALT_KEY, salt)
    return salt.encode()


def load_cache():
    if not CACHE.exists():
        return None, "MISSING"
    try:
        salt = get_or_create_salt()
        if not salt:
            return None, "TAMPERED"
        container = json.loads(CACHE.read_text())
        payload = container["payload"]
        saved = container["saved_signature"]
        payload_str = json.dumps(payload, sort_keys=True)
        expected = hmac.new(salt, payload_str.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(saved, expected):
            return None, "TAMPERED"
        start_date = datetime.date.fromisoformat(payload["start_date"])
        days_valid = int(payload["days_valid"])
        days_passed = (datetime.date.today() - start_date).days

        if days_passed >= days_valid:
            return payload, "EXPIRED"

        return payload, "VALID"

    except Exception:
        return None, "TAMPERED"



SUITS = {
    "Spades": ["running","parkour","bodybuilding"],
    "Diamonds": ["chess", "strategy", "library"],
    "Hearts": ["horror mask", "broken glass"],
    "Clubs": ["four elements", "symmetry", "duality"]
}
RANKS = ["Ace","2", "3", "4", "5", "6", "7", "8", "9", "10"]
def save_state(start_date,days_valid):
    salt = get_or_create_salt()
    payload = {
        "start_date": str(start_date),
        "days_valid": days_valid
    }
    payload_str = json.dumps(payload, sort_keys=True)
    signature = hmac.new(salt, payload_str.encode(), hashlib.sha256).hexdigest()

    container = {
        "payload": payload,
        "saved_signature": signature
    }
    CACHE.write_text(json.dumps(container, indent=4))
    DAYS_FILE.write_text(str(days_valid))
    DATE_FILE.write_text(str(start_date))
    MAIN_FILE.write_text(
        f"--- FLVX SYSTEM VISA ---\n"
        f"STATUS: ACTIVE\n"
        f"DAYS_REMAINING: {days_valid}\n"
        f"START_DATE: {start_date}\n"
        f"DO_NOT_EDIT: FALSE"
    )

def draw_card():
    suit = random.choice(list(SUITS.keys()))
    rank = random.choice(RANKS)
    days_valid = RANKS.index(rank) + 1
    queries = random.choices(SUITS[suit], k=days_valid)

    with open(DAYS_FILE, 'w') as f:
        f.write(str(days_valid))

    with open(DATE_FILE, 'w') as f:
        f.write(str(datetime.date.today()))

    return suit, rank, queries, days_valid



def draw_penalty_card():
    face_cards = [
        ("Spades", "King", 14, ["dark obsidian monolith", "deep space void"]),
        ("Hearts", "Queen", 10, ["bleeding neon", "fractured mirror portrait"]),
        ("Diamonds", "Jack", 8, ["complex quantum grid", "labyrinthine code matrix"])
    ]
    suit, rank, days_valid, queries = random.choice(face_cards)
    today = datetime.date.today()

    save_state(today, days_valid)
    return suit, rank, queries, days_valid

def run_visa_check():
    payload,statuts = load_cache()

    if statuts == "TAMPERED":
        return {"status": "PENALTY", "reason": "Tampering detected"}
    if statuts in ["EXPIRED","MISSING"]:
        return {"status": "NEW_CARD", "suit": suit, "rank": rank, "days": days_valid, "queries": queries}
    start_date = datetime.date.fromisoformat(payload["start_date"])
    days_valid = int(payload["days_valid"])
    days_passed = (datetime.date.today() - start_date).days
    true_remaining = max(0, days_valid - days_passed)

    return {
        "status": "ACTIVE",
        "days_remaining": true_remaining
    }

