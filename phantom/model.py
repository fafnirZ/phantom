"""Models."""

from __future__ import annotations
from pydantic import BaseModel
import re
from rapidfuzz import fuzz

from pyvis.network import Network as nw
import itertools


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

    def __hash__(self):
        return hash(self.__str__())


class Link(BaseModel):
    """this class models a link between 2 pages."""

    source: Page
    destination: Page
    weight: float

    def __str__(self):
        return f"Link(source={self.source}, destination={self.destination}, weight={self.weight})"

    def as_list(
        self, include_weight: bool = False
    ) -> list[Page, Page] | list[Page, Page, float]:
        if include_weight:
            return [self.source, self.destination, self.weight]
        return [self.source, self.destination]

    def as_tuple(
        self, include_weight: bool = False
    ) -> tuple[Page, Page] | tuple[Page, Page, float]:
        return tuple(self.as_list(include_weight=include_weight))


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


class Visualizer:
    def __init__(self, network: Network, output: str):
        self.viz_network = nw(
            bgcolor="#222222", height="750px", font_color="white", width="100%"
        )
        # NOTE: network keeps spazzing out
        # https://stackoverflow.com/questions/68117561/pyvis-network-keeps-on-moving
        self.viz_network.repulsion()
        self.viz_network.show_buttons(filter_=["physics"])

        # for all unique links in network
        links = [elem.as_list() for elem in network.elements]

        # list of unique Pages
        nodes = set(list(itertools.chain(*links)))
        nodes_str = [str(x) for x in nodes]

        # adding to visualisation
        self.viz_network.add_nodes(nodes_str)

        # for link tuples
        link_tuples = [link.as_tuple(include_weight=True) for link in network.elements]
        link_tuples_string = list(
            map(lambda tpl: (str(tpl[0]), str(tpl[1])), link_tuples)
        )

        self.viz_network.add_edges(link_tuples_string)

        self.viz_network.write_html(output)
