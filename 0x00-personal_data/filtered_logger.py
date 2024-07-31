#!/usr/bin/env python3
"""0. Regex-ing"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """ returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(
            pattern, lambda m: f"{m.group(1)}={redaction}{separator}", message)
