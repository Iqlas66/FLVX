import wallpaper
import visa

if __name__ == "__main__":
    result = visa.run_visa_check()
    status = result.get("status")

    if status == "PENALTY":
        print(" SECURITY BREACH: Tampering detected! Face Card penalty deployed.")
        print(" セキュリティ違反：改ざんが検知されました！絵札のペナルティが発動しました。")

        suit, rank, queries, days_valid = visa.draw_penalty_card()
        card_label = f"PENALTY: {rank} of {suit}"

        print(f"You drew the {card_label}! Your visa is locked for {days_valid} days.")
        print(f"{card_label}を引きました！あなたのビザは{days_valid}日間ロックされます。")
        wallpaper.GET_VVALLPAPER_VVALLHAVEN(queries, card_label=card_label)

    elif status == "NEW_CARD":
        suit = result["suit"]
        rank = result["rank"]
        days_valid = result["days"]
        queries = result["queries"]

        print(f"Drawn {rank} of {suit} (The visa will be active for {days_valid} days).")
        print(f"{suit}の{rank}が引かれました（ビザは{days_valid}日間有効です）")
        wallpaper.GET_VVALLPAPER_VVALLHAVEN(queries)

    elif status == "ACTIVE":
        remaining = result["days_remaining"]
        print(f"Visa is active. {remaining} days remaining.")
        print(f"ビザは有効です。残り{remaining}日。")