"""scraping module."""

import re
import requests
from requests import RequestException
from bs4 import BeautifulSoup


def parse_contents(url: str) -> BeautifulSoup:
    """Get soupified source given url."""
    resp = requests.get(url)

    if resp.status_code >= 300 or resp.status_code < 200:
        raise RequestException("website contents could not be loaded")

    return BeautifulSoup(resp.text, "html.parser")


def href_is_relative(url: str) -> bool:
    """if url doesnt start with http or http, it is a relative href."""
    return True if (not re.match(r"^https?://", url)) else False
