#!/usr/bin/env python3
"""
Module for filtering and obfuscating log messages.
"""
import re
from typing import List


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
