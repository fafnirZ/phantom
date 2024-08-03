"""Models."""

from __future__ import annotations
from pydantic import BaseModel


class Page(BaseModel):
    """this class models a webpage.

    Attributes:
        url: str
    """

    url: str


class Link(BaseModel):
    """this class models a link between 2 pages."""

    source: Page
    destination: Page


class Network(BaseModel):
    """this class contains all links."""

    elements: list[Link]
