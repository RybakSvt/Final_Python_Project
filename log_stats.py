import formatter
import connection_manager

# Console colors
RED = "\033[91m"
RESET = "\033[0m"


def get_mongo_collection():
    """Get MongoDB collection for search logs."""
    client = connection_manager.get_mongo_client()
    if client is None:
        return None

    db = client[connection_manager.MONGO_DB]
    return db[connection_manager.MONGO_COLLECTION]


def show_popular_searches():
    """Show 5 most popular searches."""
    search_logs = get_mongo_collection()
    if search_logs is None:
        print(f"{RED}⏳ Search history unavailable...{RESET}")
        formatter.wait_for_return()
        return

    # Pipeline to find popular searches
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
        print(f"{RED}⏳ Could not load statistics{RESET}")

    formatter.wait_for_return()


def show_recent_searches():
    """Show recent searches with pagination."""
    search_logs = get_mongo_collection()
    if search_logs is None:
        print(f"{RED}⏳ Search history unavailable...{RESET}")
        formatter.wait_for_return()
        return

    skip = 0
    item_number = 1

    while True:
        # Pipeline for recent searches
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
            {"$limit": 5},
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
            print(f"{RED}⏳ Could not load recent searches{RESET}")
            break

        if not results:
            break

        # Show current batch
        has_more = len(results) == 5
        formatter.print_recent_searches_batch(results, item_number, has_more)

        item_number += len(results)
        skip += 5

        # Ask to continue if there are more results
        if has_more:
            show_more = input("\nShow next 5 searches? (y/n) ").lower()
            if show_more == "n":
                break
        else:
            break

    formatter.wait_for_return()