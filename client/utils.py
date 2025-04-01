"""
Chat Client Utilities
Helper functions for the chat client
"""

import re
import emoji


def process_emoji_shortcodes(text):
    """Convert emoji shortcodes to Unicode emojis"""
    # Using the emoji library to convert shortcodes
    return emoji.emojize(text, language="alias")


def extract_urls(text):
    """Extract URLs from text and return a list of (start_pos, end_pos, url) tuples"""
    url_pattern = re.compile(r"(https?://[^\s]+)")
    urls = []

    for match in url_pattern.finditer(text):
        urls.append((match.start(), match.end(), match.group(1)))

    return urls
