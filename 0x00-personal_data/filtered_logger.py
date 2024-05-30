#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filters values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    logger.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """returns a connector to the database"""
    db_user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    mydb = mysql.connector.connect(
            host=db_host,
            user=db_user_name,
            password=db_passwd,
            database=db_name)
    return mydb


def main() -> None:
    """Read and filter data"""
    formatter = RedactingFormatter(fields=("phone",
                                           "name",
                                           "email",
                                           "ssn",
                                           "password"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        log_record = logging.LogRecord("my_logger",
                                       logging.INFO,
                                       None,
                                       None,
                                       row,
                                       None,
                                       None)
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
