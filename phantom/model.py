"""Models."""

from __future__ import annotations
from pydantic import BaseModel
import re


class Page(BaseModel):
    """this class models a webpage.

    Attributes:
        url: str
    """

    url: str

    def get_domain(self) -> str:
        """given a url is https://{domain}/..."""
        pattern = r"https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        return re.search(pattern, self.url).group(0)

    def is_page_an_asset(self) -> bool:
        """returns if the current page is an asset rather than a html website"""
        pattern = r"(.+)\.(png|svg|jpeg|pdf|csv|xlsx)"
        return True if re.match(pattern, self.url) else False


class Link(BaseModel):
    """this class models a link between 2 pages."""

    source: Page
    destination: Page
    weight: int


class Network(BaseModel):
    """this class contains all links."""

    elements: list[Link] = list()

    def add_link(self, link: Link):
        """Adds a link to Network Elements."""
        self.elements.append(link)
