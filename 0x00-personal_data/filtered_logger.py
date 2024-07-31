#!/usr/bin/env python3
"""
Module for filtering and obfuscating log messages.
"""
import re
import logging
from typing import List, Tuple
import mysql.connector
from mysql.connector import connection
import os

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Returns the log message with specified fields obfuscated.

    Args:
        fields (List[str]): list of strings with all fields to obfuscate.
        redaction (str): string representing by what the field is obfuscated
        message (str): A string representing the log line.
        separator (str): string with the character separating all fields
        in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = r'({})=[^{}]*'.format(
        '|'.join(re.escape(field) for field in fields), re.escape(separator)
    )
    return re.sub(
        pattern,
        lambda m: m.group().split('=')[0] + '=' + redaction,
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        org_msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            self.REDACTION,
                            org_msg, self.SEPARATOR
                            )


def get_logger() -> logging.Logger:
    """
     Creates a logger named "user_data" that logs up to INFO level and uses
    RedactingFormatter to obfuscate PII fields.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database.

    Returns:
        mysql.connector.connection.MySQLConnection:
        A connection to the MySQL database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
