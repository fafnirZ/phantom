"""the main function."""

from phantom.model import Page, Network, Link
from phantom.scrape import parse_contents
import time
from rapidfuzz import fuzz, process


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

    def run(self, timeout: float = 1, max_depth=1):
        """Starts the crawling process."""
        curr_depth = 0
        while len(self.queue) > 0 and curr_depth < max_depth:
            _curr: Page = self.queue.pop(0)
            if _curr in self.visited:
                continue

            if _curr.is_asset():
                continue

            self.visited.append(_curr)
            page_domain = _curr.get_domain()

            soup = parse_contents(_curr.url)

            for link in soup.find_all("a", href=True):
                # if internal link "process it accordingly"
                # print(link)

                url = link.get("href")
                print(url)
                new_page = Page(url=url)

                # TODO resolve internal link to an absolutepath

                # calculate similarity
                strength = 0
                self.network.add_link(
                    Link(source=_curr, destination=new_page, weight=strength)
                )
                self.queue.add(new_page)

            time.sleep(timeout)


if __name__ == "__main__":
    Crawl(start=Page(url="https://docs.pydantic.dev/latest/#pydantic-examples")).run()
