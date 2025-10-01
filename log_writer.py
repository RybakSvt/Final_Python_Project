from datetime import datetime
import connection_manager


def write_search_log(search_type, keyword=None, genre=None, years=None):
    """
    Save search history to MongoDB.
    Works silently - no errors if database is unavailable.
    """
    client = connection_manager.get_mongo_client()
    if client is None:
        return

    try:
        # Prepare log data
        log_data = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": {
                "keyword": keyword,
                "genre": genre,
                "year": years
            }
        }

        # Save to database
        db = client[connection_manager.MONGO_DB]
        collection = db[connection_manager.MONGO_COLLECTION]
        collection.insert_one(log_data)

    except Exception:
        pass
    finally:
        try:
            client.close()
        except:
            pass


