"""Models."""

from __future__ import annotations
from pydantic import BaseModel
import re
from rapidfuzz import fuzz, process


class Page(BaseModel):
    """this class models a webpage.

    Attributes:
        url: str
    """

    url: str

    def get_domain(self) -> str:
        """given a url is https://{domain}/..."""
        pattern = r"https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/"
        return re.search(pattern, self.url).group(0)

    def is_asset(self) -> bool:
        """returns if the current page is an asset rather than a html website"""
        pattern = r"(.+)\.(png|svg|jpeg|pdf|csv|xlsx)"
        return True if re.match(pattern, self.url) else False

    def __str__(self):
        return f"Page(url={self.url})"


class Link(BaseModel):
    """this class models a link between 2 pages."""

    source: Page
    destination: Page
    weight: float

    def __str__(self):
        return f"Link(source={self.source}, destination={self.destination}, weight={self.weight})"


class Network(BaseModel):
    """this class contains all links."""

    elements: list[Link] = list()

    def add_link(self, link: Link):
        """Adds a link to Network Elements."""
        self.elements.append(link)

    def __str__(self):
        SHOW = 10
        return (
            "Network(elements=["
            + "\n".join([f"{element}" for element in self.elements[:SHOW]])
            + "\n"
            + (f"...{len(self.elements)-SHOW} more" if len(self.elements) > 10 else "")
            + "])"
        )


class WeightUtil:
    @staticmethod
    def weight_via_url_distance(reference_str: str, target_str: str) -> float:
        return fuzz.token_ratio(reference_str, target_str)
