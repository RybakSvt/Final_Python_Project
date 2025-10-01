import log_stats
import mysql_connector
import connection_manager as cm

# Console colors
RED = "\033[91m"
RESET = "\033[0m"


def print_welcome():
    """Display welcome message and app banner."""
    print("\n🎬 Welcome to the Movie Search App! 🎬")
    print("🎞️" * 17, "\n")


def print_menu():
    """Display the main navigation menu with options."""
    print("   🎥  MOVIE SEARCH DASHBOARD  🎥")
    print("  1 — 🔍 Search by keyword")
    print("  2 — 🎭 Search by genre and years")
    print("  3 — 📊 Show popular searches")
    print("  4 — 🕒 Show recent searches")
    print("  0 — 🚪 Exit")


def handle_mysql_option(choice):
    """
    Handle movie search options (1-2).
    """
    if not cm.mysql_available:
        msg = f"{RED}⏳ Search temporarily unavailable... (Menu 1-2){RESET}"
        print(msg)
        return

    if choice == "1":
        mysql_connector.search_by_keyword()
    elif choice == "2":
        mysql_connector.search_by_genre_and_years()


def handle_mongo_option(choice):
    """
    Handle search statistics options (3-4).
    """
    if not cm.mongo_available:
        msg = f"{RED}⏳ Search history unavailable... (Menu 3-4){RESET}"
        print(msg)
        return

    if choice == "3":
        log_stats.show_popular_searches()
    elif choice == "4":
        log_stats.show_recent_searches()


def handle_invalid_input(choice):
    """
    Handle invalid user input.
    """
    if choice == "":
        print("👉 You pressed Enter. Please choose between 0 and 4")
    else:
        print("👉 Pick something between 0 and 4!")


def main():
    """Main application loop and entry point."""
    first_time = True

    while True:
        # Show welcome message on first run
        if first_time:
            print_welcome()
            first_time = False

        # Display menu options
        print_menu()

        choice = input("\nChoose action: ").strip()

        if choice in ("1", "2"):
            handle_mysql_option(choice)
        elif choice in ("3", "4"):
            handle_mongo_option(choice)
        elif choice == "0":
            print("👋 Goodbye! Hope to see you again soon!")
            break
        else:
            handle_invalid_input(choice)


if __name__ == "__main__":
    main()