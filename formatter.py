# Цвета для консоли
ORANGE_DARK = "\033[38;5;202m"
ORANGE_LIGHT = "\033[38;5;214m"
RESET = "\033[0m"


def wait_for_return():
    """Ожидание нажатия Enter для возврата в меню"""
    input("Enter → Back to the DASHBOARD: ")
    print()


def print_movies_table(cursor):
    filmes = cursor.fetchmany(10)
    if filmes:
        print("\n" + "🎬" * 20)
        print("🎥 FOUND MOVIES")
        print("🎬" * 20)
        i = 1
        while True:
            for film in filmes:
                print(f"{i:3}.\"{film[0]}\", {film[1]}, {film[2]}")
                i += 1
            filmes = cursor.fetchmany(10)
            if not filmes:
                print("🎬" * 20)
                print(f"  Total found: {i - 1} movies\n")
                wait_for_return()
                return
            show_more = input("\n🎬 Show next 10 movies ? (y/n) ").lower()
            print()
            if show_more == "n":
                return
    else:
        print("🎭 No movies found. Try another search!\n")


def print_genres_years_table(cursor):
    genres = cursor.fetchall()
    genres_dict = {}
    print("\n" + "🎬" * 16)
    print("🎥 MOVIE GENRES & YEAR RANGE")
    print("🎬" * 16)
    for i, genre in enumerate(genres, start=1):
        genres_dict[genre[0]] = [genre[1], genre[2]]
        print(f"{i:3}. {genre[0]:15} {genre[1]} - {genre[2]}")
    print("🎬" * 16)
    return genres_dict


def print_popular_searches(results):
    """Красивый вывод популярных поисков"""
    print("\n" + "🔥" * 24)
    print("📊 TOP 5 POPULAR SEARCHES")
    print("🔥" * 24)

    for i, search in enumerate(results, start=1):
        search_type = search["search_type"]
        count = search["count"]

        if search_type == "keyword":
            display = f"Keyword: {ORANGE_DARK}{search['keyword']}{RESET}"
        elif search_type == "genre_years":
            display = f"Genre:   {ORANGE_LIGHT}{search['genre']}, Years: {search['years']}{RESET}"
        else:
            display = f"Search type: {search_type}"

        print(f"{i:2}. {display} - {count} searches")
    print("🔥" * 24)


def print_recent_searches_batch(results, start_number, has_more):
    """Вывод партии последних поисков"""
    if start_number == 1:
        print("\n" + "🕒" * 18)
        print("📋 RECENT SEARCHES")
        print("🕒" * 18)

    for j, search in enumerate(results, start_number):
        search_type = search["search_type"]
        date = search["last_date"].strftime("%Y-%m-%d")
        count = search["count"]

        if search_type == "keyword":
            display = f"Keyword: {ORANGE_DARK}{search['keyword']}{RESET}"
        elif search_type == "genre_years":
            display = f"Genre: {ORANGE_LIGHT}{search['genre']}, Years: {search['years']}{RESET}"

        print(f"{j:3}. {display}")
        print(f"     Date: {date} | Times: {count}")

    if not has_more:
        print("🕒" * 16)
        print(f"Total shown: {start_number + len(results) - 1} searches\n")