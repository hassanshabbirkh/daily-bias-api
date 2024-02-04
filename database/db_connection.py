import sqlite3
from sqlite3 import Error

class DatabaseConnection:
    _instance = None
    DB_PATH = "/home/hassan/synap-tech/production-database.db"  # Class variable for DB path

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._instance.connection = sqlite3.connect(cls.DB_PATH)  # Use class variable
            except Error as e:
                print(e)
        return cls._instance

    @classmethod
    def get_connection(cls):
        return cls._instance.connection

    @classmethod
    def close_connection(cls):
        if cls._instance is not None:
            cls._instance.connection.close()
