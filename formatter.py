# Console colors
ORANGE_DARK = "\033[38;5;202m"
ORANGE_LIGHT = "\033[38;5;214m"
RESET = "\033[0m"

# Display constants
MOVIES_BATCH_SIZE = 10
BORDER_LENGTH = 16


def wait_for_return():
    """Wait for Enter key to return to main menu."""
    input("Enter → Back to the DASHBOARD: ")
    print()


def _print_header(title, symbol, length=20):
    """Print formatted header with borders."""
    print(f"\n{symbol * length}")
    print(f"🎥 {title}")
    print(f"{symbol * length}")


def _print_footer(symbol, length=20):
    """Print formatted footer."""
    print(f"{symbol * length}")


def print_movies_table(cursor):
    """Display movies in batches of 10 with pagination."""
    movies = cursor.fetchmany(MOVIES_BATCH_SIZE)

    if not movies:
        print("🎭 No movies found. Try another search!\n")
        return

    _print_header("FOUND MOVIES", "🎬")

    movie_count = 1
    while True:
        # Display current batch
        for movie in movies:
            print(f"{movie_count:3}. \"{movie[0]}\", {movie[1]}, {movie[2]}")
            movie_count += 1

        # Get next batch
        movies = cursor.fetchmany(MOVIES_BATCH_SIZE)

        if not movies:
            _print_footer("🎬")
            print(f"  Total found: {movie_count - 1} movies\n")
            wait_for_return()
            return

        # Ask to continue
        show_more = input("\n🎬 Show next 10 movies? (y/n) ").lower()
        print()
        if show_more == "n":
            return


def print_genres_years_table(cursor):
    """Display movie genres with their year ranges."""
    genres = cursor.fetchall()
    genres_dict = {}

    _print_header("MOVIE GENRES & YEAR RANGE", "🎬", BORDER_LENGTH)

    for i, genre in enumerate(genres, start=1):
        genres_dict[genre[0]] = [genre[1], genre[2]]
        print(f"{i:3}. {genre[0]:15} {genre[1]} - {genre[2]}")

    _print_footer("🎬", BORDER_LENGTH)
    return genres_dict


def _format_search_display(search):
    """Format search entry for display with colors."""
    search_type = search["search_type"]

    if search_type == "keyword":
        return f"Keyword: {ORANGE_DARK}{search['keyword']}{RESET}"
    elif search_type == "genre_years":
        text = f"Genre: {ORANGE_LIGHT}{search['genre']}, Years: {search['years']}{RESET}"
        return text
    else:
        return f"Search type: {search_type}"


def print_popular_searches(results):
    """Display top 5 most popular searches."""
    _print_header("TOP 5 POPULAR SEARCHES", "🔥", 24)

    for i, search in enumerate(results, start=1):
        display = _format_search_display(search)
        count = search["count"]
        print(f"{i:2}. {display} - {count} searches")

    _print_footer("🔥", 24)


def print_recent_searches_batch(results, start_number, has_more):
    """Display a batch of recent searches."""
    if start_number == 1:
        _print_header("RECENT SEARCHES", "🕒", 18)

    for j, search in enumerate(results, start_number):
        display = _format_search_display(search)
        date = search["last_date"].strftime("%Y-%m-%d")
        count = search["count"]

        print(f"{j:3}. {display}")
        print(f"     Date: {date} | Times: {count}")

    if not has_more:
        _print_footer("🕒", BORDER_LENGTH)
        total = start_number + len(results) - 1
        print(f"Total shown: {total} searches\n")