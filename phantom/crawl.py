"""the main function."""

from pydantic import BaseModel
from phantom.model import Page


class Crawl(BaseModel):
    """given a base Page start crawling using a BFS algorithm."""

    start: Page
    queue: Page = []
