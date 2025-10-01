from pymongo import errors
from datetime import datetime
import connection_manager


def write_search_log(search_type, keyword=None, genre=None, years=None):
    client = connection_manager.get_mongo_client()
    if client is None:
        return  # выход если MongoDB недоступна

    try:
        client = connection_manager.get_mongo_client()
        if client is None:
            return

        db_name = client[connection_manager.MONGO_DB]
        logs = db_name[connection_manager.MONGO_COLLECTION]

        log = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": {
                "keyword": keyword,
                "genre": genre,
                "year": years
            }
        }

        logs.insert_one(log)

    except errors.PyMongoError:
        pass     # Игнорируем ошибки MongoDB
    except Exception:
        pass     # Игнорируем все остальные ошибки
    finally:
        try:
            client.close()
        except:
            pass



