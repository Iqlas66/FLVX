import json
import datetime
from pathlib import Path
import random
import keyring
from cryptography.fernet import Fernet, InvalidToken

SERVICE_NAME = "FLVX_Borderland_System"
SALT_KEY = "encryption_salt"
KEY_NAME = "TOPPRIORITY"
CACHE = Path(".flux_core_cache.dat")
MAIN_FILE = Path("visa.txt")
DATE_FILE = Path("dates.txt")
DAYS_FILE = Path("days_valid.txt")

SUITS = {
    "Spades": ["running","parkour","bodybuilding"],
    "Diamonds": ["chess", "strategy", "library"],
    "Hearts": ["horror mask", "broken glass"],
    "Clubs": ["four elements", "symmetry", "duality"]
}
RANKS = ["Ace","2", "3", "4", "5", "6", "7", "8", "9", "10"]
def get_or_create_key():
    key = keyring.get_password(SERVICE_NAME, KEY_NAME)

    if key:
        try:
            key_bytes = key.encode() if isinstance(key, str) else key
            Fernet(key_bytes)
            return key_bytes
        except Exception:
            pass


    new_key = Fernet.generate_key()
    keyring.set_password(SERVICE_NAME, KEY_NAME, new_key.decode())
    return new_key






def load_cache():
    if not CACHE.exists():
        return None, "MISSING"
    try:
        key = get_or_create_key()
        f = Fernet(key)
        encrypted_data = CACHE.read_bytes()
        decrypted_data = f.decrypt(encrypted_data)
        payload = json.loads(decrypted_data.decode())
        start_date = datetime.date.fromisoformat(payload["start_date"])
        days_valid = int(payload["days_valid"])
        days_passed = (datetime.date.today() - start_date).days
        if days_passed >= days_valid:
            return payload, "EXPIRED"

        return payload, "VALID"

    except (InvalidToken, Exception):
        return None, "TAMPERED"



def save_state(start_date,days_valid):
    key = get_or_create_key()
    f = Fernet(key)

    payload = {
        "start_date": str(start_date),
        "days_valid": days_valid
    }
    payload_str = json.dumps(payload, sort_keys=True).encode()
    encrypted_data = f.encrypt(payload_str)

    CACHE.write_bytes(encrypted_data)

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
    today = datetime.date.today()
    save_state(today, days_valid)

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
    suit, rank, queries, days_valid = draw_card()

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

