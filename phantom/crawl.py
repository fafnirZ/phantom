"""the main function."""

from requests import RequestException
from phantom.model import Page, Network, Link, Visualizer, WeightUtil
from phantom.scrape import parse_contents, href_is_relative
import time


class Crawl:
    """given a base Page start crawling using a BFS algorithm."""

    start: Page
    queue: Page = []
    visited: Page = []
    network: Network = Network()

    def __init__(self, start: Page):
        """Init function."""
        self.start = start
        self.queue.append(self.start)

    def run(self, timeout: float = 1, max_depth=2):
        """Starts the crawling process."""
        curr_depth = 0
        while len(self.queue) > 0 and curr_depth < max_depth:
            _curr: Page = self.queue.pop(0)
            curr_depth += 1

            if _curr in self.visited:
                continue

            if _curr.is_asset():
                continue

            self.visited.append(_curr)
            page_domain = _curr.get_domain()

            try:
                soup = parse_contents(_curr.url)
            except RequestException:
                continue

            for link in soup.find_all("a", href=True):
                # if internal link "process it accordingly"
                url = link.get("href")

                # resolve internal link to an absolutepath
                if href_is_relative(url):
                    _url = url
                    url = f"{page_domain}{_url}"

                new_page = Page(url=url)

                # calculate similarity
                strength = WeightUtil.weight_via_url_distance(
                    self.start.url, new_page.url
                )
                self.network.add_link(
                    Link(source=_curr, destination=new_page, weight=strength)
                )
                self.queue.append(new_page)

            time.sleep(timeout)

        Visualizer(self.network)


if __name__ == "__main__":
    Crawl(start=Page(url="https://docs.pydantic.dev/latest/#pydantic-examples")).run()
