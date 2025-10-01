import log_stats
import mysql_connector
import connection_manager as cm

# Цвета для консоли
RED = "\033[91m"
RESET = "\033[0m"


first_time = True

while True:
    if first_time:
        print("\n🎬  Welcome to the Movie Search App! 🎬")
        print("🎞️" * 17,"\n")
        first_time = False

    print("   🎥  MOVIE SEARCH DASHBOARD  🎥")
    print("  1 — 🔍 Search by keyword")
    print("  2 — 🎭 Search by genre and years")
    print("  3 — 📊 Show popular searches")
    print("  4 — 🕒 Show recent searches")
    print("  0 — 🚪Exit")

    choice = input("\nChoose action: ").strip()

    if choice == "1":
        if cm.mysql_available:
            mysql_connector.search_by_keyword()
        else:
            print(f"{RED}⏳ Search temporarily unavailable... (Menu 1-2){RESET}")

    elif choice == "2":
        if cm.mysql_available:
            mysql_connector.search_by_genre_and_years()
        else:
            print(f"{RED}⏳ Search temporarily unavailable... (Menu 1-2){RESET}")

    elif choice == "3":
        if cm.mongo_available:
            log_stats.show_popular_searches()
        else:
            print(f"{RED}⏳ Search history temporarily unavailable... (Menu 3-4){RESET}")

    elif choice == "4":
        if cm.mongo_available:
            log_stats.show_recent_searches()
        else:
            print(f"{RED}⏳ Search history temporarily unavailable... (Menu 3-4){RESET}")

    elif choice == "0":
        print("👋 Goodbye! Hope to see you again soon!")
        break

    elif choice == "":
        print("👉 You pressed Enter. Please choose between 0 and 4 ")

    else:
        print("👉 Pick something between 0 and 4!")