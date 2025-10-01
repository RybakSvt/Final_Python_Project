import os
import pymysql
import dotenv
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime

# Load environment variables once
dotenv.load_dotenv(Path('.env'))

# Database configuration
MYSQL_CONFIG = {
    'host': os.environ.get('HOST'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'database': 'sakila'
}

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")


def write_log(message):
    """Write message to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("db_connections.log", 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")


def check_mysql_connection():
    """Check if MySQL is available."""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        connection.close()
        write_log("MySQL connection successful")
        return True
    except pymysql.Error as e:
        write_log(f"MySQL connection failed: {e}")
        return False


def check_mongo_connection():
    """Check if MongoDB is available."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        client.close()
        write_log("MongoDB connection successful")
        return True
    except Exception as e:
        write_log(f"MongoDB connection failed: {e}")
        return False


def get_mysql_connection():
    """Get MySQL connection for queries."""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        write_log("MySQL get_connection successful")
        return connection
    except pymysql.Error as e:
        write_log(f"MySQL get_connection failed: {e}")
        return None


def get_mongo_client():
    """Get MongoDB client for queries."""
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,           # 5s max to select MongoDB server
            connectTimeoutMS=5000                    # 5s max for TCP connection setup
        )
        client.admin.command('ping')
        write_log("MongoDB get_client successful")
        return client
    except Exception as e:
        write_log(f"MongoDB get_client failed: {e}")
        return None


# Check database availability on startup
mysql_available = check_mysql_connection()
mongo_available = check_mongo_connection()
