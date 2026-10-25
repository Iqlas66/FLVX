import json
import datetime
from pathlib import Path
import random
import keyring
from cryptography.fernet import Fernet, InvalidToken

SERVICE_NAME = "FLVX_Borderland_System"
KEY_NAME = "TOPPRIORITY"

CACHE = Path(".flux_core_cache.dat") #CACHE
MAIN_FILE = Path("visa.txt")
DATE_FILE = Path("dates.txt")
DAYS_FILE = Path("days_valid.txt")

SUITS = {
    "Spades": ["running", "parkour", "bodybuilding"],
    "Diamonds": ["chess", "strategy", "library"],
    "Hearts": ["horror mask", "broken glass"],
    "Clubs": ["four elements", "symmetry", "duality"]
}

RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def get_or_create_key():
    key = keyring.get_password(SERVICE_NAME, KEY_NAME) #Gets key
    if key:
        try:
            key_bytes = key.encode() if isinstance(key, str) else key
            Fernet(key_bytes)
            return key_bytes
        except Exception:
            pass

    new_key = Fernet.generate_key()  #Creates new if nonexistant
    keyring.set_password(SERVICE_NAME, KEY_NAME, new_key.decode()) #Applies the key
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


def save_state(start_date, days_valid, queries, suit=None, rank=None, last_download_date=None):
    key = get_or_create_key()
    f = Fernet(key)

    payload = {
        "start_date": str(start_date),
        "days_valid": days_valid,
        "queries": queries,
        "suit": suit,
        "rank": rank,
        "last_download_date": str(last_download_date or datetime.date.today())
    }
    payload_str = json.dumps(payload, sort_keys=True).encode()
    encrypted_data = f.encrypt(payload_str) #encrypts the data
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
    suit = random.choice(list(SUITS.keys())) #Selects random suit
    rank = random.choice(RANKS)#Selects random rank
    days_valid = RANKS.index(rank) + 1
    queries = random.choices(SUITS[suit], k=days_valid)
    today = datetime.date.today()
    save_state(today, days_valid, queries, suit, rank, today)
    return suit, rank, queries, days_valid


def draw_penalty_card():
    face_cards = [
        ("Spades", "King", 14, ["dark obsidian monolith", "deep space void"]),
        ("Hearts", "Queen", 10, ["bleeding neon", "fractured mirror portrait"]),
        ("Diamonds", "Jack", 8, ["complex quantum grid", "labyrinthine code matrix"])
    ]
    suit, rank, days_valid, queries = random.choice(face_cards)
    today = datetime.date.today()
    save_state(today, days_valid, queries, suit, rank, today)
    return suit, rank, queries, days_valid


def run_visa_check():
    payload, status = load_cache()

    if status == "TAMPERED":
        return {"status": "PENALTY", "reason": "Tampering detected", "download_needed": True}

    if status in ["EXPIRED", "MISSING"]:
        suit, rank, queries, days_valid = draw_card()
        return {
            "status": "NEW_CARD",
            "suit": suit,
            "rank": rank,
            "days": days_valid,
            "queries": queries,
            "download_needed": True
        }

    start_date = datetime.date.fromisoformat(payload["start_date"])
    days_valid = int(payload["days_valid"])
    queries = payload.get("queries", ["default query"])
    suit = payload.get("suit", "Unknown")
    rank = payload.get("rank", "Unknown")
    last_download = payload.get("last_download_date", "")

    today = datetime.date.today()
    days_passed = (today - start_date).days
    true_remaining = max(0, days_valid - days_passed)

    day_index = min(days_passed, len(queries) - 1)
    todays_query = queries[day_index]
    download_needed = str(today) != last_download

    if download_needed:
        save_state(start_date, days_valid, queries, suit, rank, today) #saves states

    return {
        "status": "ACTIVE",
        "days_remaining": true_remaining,
        "query": todays_query,
        "suit": suit,
        "rank": rank,
        "download_needed": download_needed
    }


def get_card_code(rank, suit):
    rank_str = str(rank)
    if rank_str.isdigit():
        r_code = rank_str[-1]  #if its a digit reterns the last character
    else:
        r_code = rank_str[0].upper() #if its  a word then the first one

    s_code = suit[0].upper()
    return f"{r_code}{s_code}"



#なぜこんなことをしているの？
#ここは見てはいけないことになっています。
#〜じゃないの？