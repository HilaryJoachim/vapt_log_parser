import datetime

def generate_daily_error_summary():
    today = datetime.date.today().isoformat()
    print("\n=== DAILY ERROR SUMMARY ===\n")

    try:
        with open("error_reports.log", "r") as f:
            found = False
            for line in f:
                if today in line:
                    print(line.strip())
                    found = True

        if not found:
            print("No errors recorded today.")

    except FileNotFoundError:
        print("⚠ error_reports.log not found.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    generate_daily_error_summary()
