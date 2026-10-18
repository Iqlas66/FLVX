import random
import datetime
from pathlib import Path

DATE_FILE = Path("dates.txt")
DAYS_FILE = Path("days_valid.txt")

SUITS = {
    "Spades": ["nebula", "mars surface landscape", "deep space galaxy", "supernova"],
    "Diamonds": ["cyberpunk architecture", "minimalist geometry", "tech circuit"],
    "Hearts": ["moody portrait", "dramatic sunset", "vibrant neon"],
    "Clubs": ["abstract balance", "symmetry", "dual tone"]
}
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

def draw_card():
    suit = random.choice(list(SUITS.keys()))
    rank = random.choice(RANKS)
    days_valid = RANKS.index(rank) + 2
    queries = random.choices(SUITS[suit], k=days_valid)

    with open(DAYS_FILE, 'w') as f:
        f.write(str(days_valid))

    return suit, rank, queries, days_valid

def is_expired():
    file = Path(DAYS_FILE)
    if file.exists() and DATE_FILE.exists():
        with open(DAYS_FILE, 'r') as f:
            days_valid = int(f.read())
        last_date = datetime.date.fromisoformat(DATE_FILE.read_text().strip())
        return (datetime.date.today() - last_date).days >= days_valid
    else:
        return True

def get_days_remaining():
    if DAYS_FILE.exists() and DATE_FILE.exists():
        try:
            days_valid = int(DAYS_FILE.read_text().strip())
            last_date = datetime.date.fromisoformat(DATE_FILE.read_text().strip())
            days_passed  =  (datetime.date.today() - last_date).days
            remaining = days_valid - days_passed
            return max(0, remaining)
        except ValueError:
            return 0
    return 0