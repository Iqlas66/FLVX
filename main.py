import json
import visa
import threading
if __name__ == "__main__":
    result = visa.run_visa_check()
    status = result.get("status")
    frontend_data = {}
    queries_to_download = []

    download_needed = result.get("download_needed", True)

    if status == "PENALTY":
        suit, rank, queries, days_valid = visa.draw_penalty_card()
        card_label = f"Penalty: {rank} of {suit}"
        queries_to_download = queries
        card_code = visa.get_card_code(rank, suit)
        image_url = f"https://deckofcardsapi.com/static/img/{card_code}.png"

        frontend_data = {
            "status": "PENALTY",
            "suit": suit,
            "rank": rank,
            "days_valid": days_valid,
            "query": queries[0],
            "label": card_label,
            "image_url": image_url
        }

    elif status == "NEW_CARD":
        suit = result['suit']
        rank = result['rank']
        days_valid = result['days']
        queries = result['queries']
        queries_to_download = queries
        card_code = visa.get_card_code(rank, suit)
        image_url = f"https://deckofcardsapi.com/static/img/{card_code}.png"

        frontend_data = {
            "status": "NEW_CARD",
            "suit": suit,
            "rank": rank,
            "days_valid": days_valid,
            "query": queries[0],
            "image_url": image_url
        }

    elif status == "ACTIVE":
        remaining = result['days_remaining']
        todays_query = result['query']
        suit = result.get('suit', 'Unknown')
        rank = result.get('rank', 'Unknown')
        queries_to_download = [todays_query]
        card_code = visa.get_card_code(rank, suit)
        image_url = f"https://deckofcardsapi.com/static/img/{card_code}.png"

        frontend_data = {
            "status": "ACTIVE",
            "days_remaining": remaining,
            "query": todays_query,
            "suit": suit,
            "rank": rank,
            "image_url": image_url
        }

    print(json.dumps(frontend_data), flush=True)

    if download_needed:
        try:
            import wallpaper
            def bg_download():
                try:
                    wallpaper.GET_VVALLPAPER_VVALLHAVEN(queries_to_download)
                except:
                    pass
            t = threading.Thread(target=bg_download)
            t.start()
            t.join()
        except Exception:
            pass