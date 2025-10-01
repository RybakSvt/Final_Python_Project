import os
import pymysql
import dotenv
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime
from pymongo import errors


dotenv.load_dotenv(Path('.env'))

MYSQL_CONFIG = {
    'host': os.environ.get('HOST'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'database': 'sakila'
}

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")

def _write_log(message):
    """Записывает сообщение в лог-файл"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("db_connections.log", 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def check_mysql_connection():
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        connection.close()
        _write_log("MySQL connection successful")
        return True
    except pymysql.Error as e:
        _write_log(f"MySQL connection failed: {e}")
        return False

def check_mongo_connection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        client.close()
        _write_log("MongoDB connection successful")
        return True
    except Exception as e:
        _write_log(f"MongoDB connection failed: {e}")
        return False

def get_mysql_connection():
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        _write_log("MySQL get_connection successful")
        return connection
    except pymysql.Error as e:
        _write_log(f"MySQL get_connection failed: {e}")
        return None

def get_mongo_client():
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        client.admin.command('ping')
        _write_log("MongoDB get_client successful")
        return client
    except errors.ServerSelectionTimeoutError as e:
        _write_log(f"MongoDB connection timeout: {e}")
        return None
    except errors.ConnectionFailure as e:
        _write_log(f"MongoDB connection failed: {e}")
        return None
    except errors.PyMongoError as e:
        _write_log(f"MongoDB error: {e}")
        return None

# Глобальные переменные доступности
mysql_available = check_mysql_connection()
mongo_available = check_mongo_connection()
