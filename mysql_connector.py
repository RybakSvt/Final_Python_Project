import pymysql
import formatter
import log_writer
import connection_manager


def execute_query(query, params=None):
    """Выполняет SQL запрос и возвращает курсор"""
    connection = connection_manager.get_mysql_connection()
    if connection is None:
        return None, None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or {})
        return connection, cursor
    except pymysql.Error as e:
        print("⏳ Search service is currently busy... Please try again")
        connection.close()
        return None, None


def search_by_keyword():
    keyword = input("Enter keyword for search: ")
    log_writer.write_search_log("keyword", keyword=keyword)

    query = """
            SELECT title, release_year, name, description
            FROM film AS f
                     JOIN film_category AS fc ON f.film_id = fc.film_id
                     JOIN category AS c ON fc.category_id = c.category_id
            WHERE title LIKE %(keyword)s
            ORDER BY title ASC 
            """

    connection, cursor = execute_query(query, {"keyword": f"%{keyword}%"})

    if cursor is None:
        return

    formatter.print_movies_table(cursor)
    cursor.close()
    connection.close()
    return


def search_by_genre_and_years():
    query = """
            SELECT c.name              AS category_name,
                   MIN(f.release_year) AS min_release_year,
                   MAX(f.release_year) AS max_release_year
            FROM film AS f
                     JOIN film_category AS fc ON f.film_id = fc.film_id
                     JOIN category AS c ON fc.category_id = c.category_id
            GROUP BY c.name
            ORDER BY c.name 
            """

    connection, cursor = execute_query(query)

    if cursor is None:
        return

    genres_dict = formatter.print_genres_years_table(cursor)
    cursor.close()
    connection.close()

    selected_genre = get_genre_by_prefix(genres_dict)

    if selected_genre is None:
        return  # пользователь нажал Enter

    min_year = genres_dict[selected_genre][0]
    max_year = genres_dict[selected_genre][1]

    while True:
        years_input = input(f"Enter year or range ({min_year} - {max_year}): ").strip()
        years, error = validate_years(years_input, min_year, max_year)

        if error:
            print(f" {error}")
            continue

        start_year, end_year = years
        break

    log_writer.write_search_log("genre_years", genre=selected_genre, years=years_input)

    movies_query = """
                   SELECT f.title,
                          f.release_year,
                          c.name AS genre,
                          f.description
                   FROM film AS f
                            JOIN film_category AS fc ON f.film_id = fc.film_id
                            JOIN category AS c ON fc.category_id = c.category_id
                   WHERE c.name = %(genre)s
                     AND f.release_year BETWEEN %(start_year)s AND %(end_year)s
                   ORDER BY f.title ASC 
                   """

    connection, cursor = execute_query(movies_query, {
        "genre": selected_genre,
        "start_year": start_year,
        "end_year": end_year
    })

    if cursor is not None:
        formatter.print_movies_table(cursor)
        cursor.close()
        connection.close()


def get_genre_by_prefix(genres_dict):
    """Получает жанр по первым 3 буквам (и более) с проверкой ввода"""
    while True:
        genre = input("Enter first 3 letters of genre (or Enter to return): ").strip()
        if genre == "":
            return None
        if len(genre) < 3:
            print("Please enter at least 3 characters")
            continue

        genre_prefix = genre[:3].lower()
        matching_genres = [key for key in genres_dict.keys() if key[:3].lower() == genre_prefix]

        if not matching_genres:
            print(f"No genres found starting with '{genre_prefix}'")
            available_genres = ", ".join(genres_dict.keys())
            print(f"Available: {available_genres}")
        elif len(matching_genres) == 1:
            return matching_genres[0]


def validate_years(input_years, min_year, max_year):
    """Проверяет и преобразует ввод года/диапазона"""
    input_years = input_years.replace(" ", "")

    if '-' in input_years:
        parts = input_years.split('-')
        if len(parts) != 2:
            return None, "Invalid range format. Use: YYYY-YYYY"

        start_year, end_year = parts

        if not (start_year.isdigit() and end_year.isdigit()):
            return None, "Years must be 4-digit numbers"
        if len(start_year) != 4 or len(end_year) != 4:
            return None, "Years must be 4-digit numbers"

        start_year = int(start_year)
        end_year = int(end_year)

        if start_year > end_year:
            return None, "Start year cannot be greater than end year"
        if start_year < min_year or end_year > max_year:
            return None, f"Years must be between {min_year} and {max_year}"

        return (start_year, end_year), None

    else:
        if not input_years.isdigit():
            return None, "Year must be a 4-digit number"
        if len(input_years) != 4:
            return None, "Year must be a 4-digit number"

        year = int(input_years)

        if year < min_year or year > max_year:
            return None, f"Year must be between {min_year} and {max_year}"

        return (year, year), None


