import formatter
import connection_manager

# Цвета для консоли
RED = "\033[91m"
RESET = "\033[0m"


def get_mongo_collection():
    """Возвращает коллекцию MongoDB для работы с логами"""
    client = connection_manager.get_mongo_client()
    if client is None:
        return None

    db_name = client[connection_manager.MONGO_DB]
    return db_name[connection_manager.MONGO_COLLECTION]


def show_popular_searches():
    search_logs = get_mongo_collection()
    if search_logs is None:
        print(f"{RED}⏳ Search history temporarily unavailable... (Menu 3-4){RESET}")
        formatter.wait_for_return()
        return

    pipeline = [
        {"$group": {
            "_id": {
                "search_type": "$search_type",
                "keyword": "$params.keyword",
                "genre": "$params.genre",
                "years": "$params.year"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 5},
        {"$project": {
            "search_type": "$_id.search_type",
            "keyword": "$_id.keyword",
            "genre": "$_id.genre",
            "years": "$_id.years",
            "count": 1,
            "_id": 0
        }}
    ]

    try:
        results = list(search_logs.aggregate(pipeline))
        formatter.print_popular_searches(results)
    except Exception:
        print(f"{RED}⏳ Could not load search statistics...{RESET}")

    formatter.wait_for_return()
    return


def show_recent_searches():
    """Показывает последние уникальные запросы"""
    search_logs = get_mongo_collection()
    if search_logs is None:
        print(f"{RED}⏳ Search history temporarily unavailable... (Menu 3-4){RESET}")
        formatter.wait_for_return()
        return

    skip = 0
    limit = 5
    i = 1

    while True:
        pipeline = [
            {"$sort": {"timestamp": -1}},
            {"$group": {
                "_id": {
                    "search_type": "$search_type",
                    "keyword": "$params.keyword",
                    "genre": "$params.genre",
                    "years": "$params.year"
                },
                "last_date": {"$last": "$timestamp"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"last_date": -1}},
            {"$skip": skip},
            {"$limit": limit},
            {"$project": {
                "search_type": "$_id.search_type",
                "keyword": "$_id.keyword",
                "genre": "$_id.genre",
                "years": "$_id.years",
                "last_date": 1,
                "count": 1,
                "_id": 0
            }}
        ]

        try:
            results = list(search_logs.aggregate(pipeline))
        except Exception:
            print(f"{RED}⏳ Could not load recent searches...{RESET}")
            break

        if not results:
            break

        formatter.print_recent_searches_batch(results, i, len(results) == limit)

        i += len(results)
        skip += limit

        # Если есть еще результаты, спрашиваем продолжить
        if len(results) == limit:
            show_more = input("\nShow next 5 searches? (y/n) ").lower()
            if show_more == "n":
                break
        else:
            break

    formatter.wait_for_return()