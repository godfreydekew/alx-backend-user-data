#!/usr/bin/env python3
"""0. Regex-ing"""
import re
from typing import List
import logging


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """ returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(
            pattern, lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the logg data and hides private info"""
        message = super().format(record)
        for field in self.fields:
            message = re.sub(
                    rf'{field}=[^;]*', f'{field}={self.REDACTION}', message)
        return message
