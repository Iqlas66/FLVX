import wallpaper
import visa


if __name__ == "__main__":
    if visa.is_expired():
        suit, rank, queries, days_valid = visa.draw_card()
        print(f"Drawn {rank} of {suit} (The visa will be active for {days_valid} days).")
        print(f"{suit}の{rank}が引かれました（ビザは{days_valid}日間有効です）")
        for i, query in enumerate(queries):
            wallpaper.GET_VVALLPAPER_VVALLHAVEN(queries)

    else:
        remaining = visa.get_days_remaining()
        print(f"Visa is active. {remaining} days remaining.")
        print(f"ビザは有効です。残り{remaining}日。")



