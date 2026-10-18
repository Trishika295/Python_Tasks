
import csv
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


# ==================================================
# CONFIGURATION
# ==================================================

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = Path(__file__).parent / "scraped_data.csv"

USER_AGENT = "BookScopeEducationalScraper/1.0"
REQUEST_DELAY = 1.0
TIMEOUT = 20

FIELDS = [
    "title",
    "price",
    "availability",
    "rating",
    "product_url",
    "image_url",
    "page_number",
]


# ==================================================
# URL VALIDATION
# ==================================================

def validate_url(url):
    """Accept only HTTPS URLs on the practice website."""

    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or parsed.hostname != "books.toscrape.com"
        or parsed.username
        or parsed.password
    ):
        raise ValueError(
            "For this project, use HTTPS URLs from "
            "books.toscrape.com only."
        )


# ==================================================
# ROBOTS.TXT CHECK
# ==================================================

def check_robots_permission(url):
    """
    Check robots.txt before scraping.

    A 404 response is reported separately. It does not
    establish general permission to scrape a website.
    """

    validate_url(url)

    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )

        if response.status_code == 404:
            return (
                True,
                "robots.txt was not found (404). This is the "
                "designated educational practice website; "
                "a missing robots.txt is not proof of permission. "
                "Use only for permitted practice and respect "
                "the website's terms.",
            )

        if response.status_code in (401, 403):
            return (
                False,
                f"Access to robots.txt was denied "
                f"(HTTP {response.status_code}). Scraping stopped.",
            )

        response.raise_for_status()

        parser = RobotFileParser()
        parser.parse(response.text.splitlines())

        if not parser.can_fetch(USER_AGENT, url):
            return (
                False,
                "robots.txt disallows scraping this URL.",
            )

        return True, "robots.txt permits this URL."

    except requests.RequestException as error:
        return (
            False,
            f"Could not verify robots.txt: {error}. "
            "Scraping stopped for safety.",
        )


# ==================================================
# DOWNLOAD HTML
# ==================================================

def fetch_html(url):
    """Download a webpage and return its HTML."""

    validate_url(url)

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type.lower():
        raise ValueError("The URL did not return an HTML page.")

    return response.text


# ==================================================
# PARSE BOOK INFORMATION
# ==================================================

def parse_books(html, page_url, page_number):
    """Extract book details and the next-page URL."""

    soup = BeautifulSoup(html, "html.parser")
    records = []

    for book in soup.select("article.product_pod"):

        link = book.select_one("h3 a")
        price = book.select_one(".price_color")
        availability = book.select_one(".availability")
        rating_element = book.select_one(".star-rating")
        image = book.select_one("img")

        if link is None:
            continue

        title = (
            link.get("title")
            or link.get_text(strip=True)
        )

        product_url = urljoin(
            page_url,
            link.get("href", ""),
        )

        image_url = ""

        if image and image.get("src"):
            image_url = urljoin(
                page_url,
                image["src"],
            )

        rating = ""

        if rating_element:
            rating = next(
                (
                    name
                    for name in rating_element.get("class", [])
                    if name != "star-rating"
                ),
                "",
            )

        records.append({
            "title": title,
            "price": (
                price.get_text(strip=True)
                if price else ""
            ),
            "availability": (
                availability.get_text(" ", strip=True)
                if availability else ""
            ),
            "rating": rating,
            "product_url": product_url,
            "image_url": image_url,
            "page_number": page_number,
        })

    next_link = soup.select_one("li.next a")

    next_url = (
        urljoin(page_url, next_link.get("href", ""))
        if next_link else None
    )

    return records, next_url


# ==================================================
# MAIN SCRAPER
# ==================================================

def scrape_website(
    start_url=BASE_URL,
    max_pages=1,
    progress=None,
):
    """
    Scrape multiple catalog pages.

    This function signature matches app.py exactly.
    Returns: records, permission_message, pages_scraped
    """

    validate_url(start_url)

    if (
        not isinstance(max_pages, int)
        or isinstance(max_pages, bool)
        or not 1 <= max_pages <= 10
    ):
        raise ValueError(
            "Select between 1 and 10 pages."
        )

    allowed, permission_message = check_robots_permission(
        start_url
    )

    if not allowed:
        raise PermissionError(permission_message)

    records = []
    current_url = start_url
    visited_urls = set()
    pages_scraped = 0

    for page_number in range(1, max_pages + 1):

        if not current_url:
            break

        validate_url(current_url)

        if current_url in visited_urls:
            break

        visited_urls.add(current_url)

        if progress:
            progress(
                f"Scraping catalog page {page_number} "
                f"of {max_pages}...",
                (page_number - 1) / max_pages,
            )

        if page_number > 1:
            time.sleep(REQUEST_DELAY)

        html = fetch_html(current_url)

        page_records, next_url = parse_books(
            html,
            current_url,
            page_number,
        )

        if not page_records:
            break

        records.extend(page_records)
        pages_scraped += 1
        current_url = next_url

    if not records:
        raise ValueError(
            "No books were extracted. Check the catalog URL "
            "or whether its HTML structure has changed."
        )

    if progress:
        progress("Scraping completed successfully.", 1.0)

    return records, permission_message, pages_scraped


# ==================================================
# SAVE CSV
# ==================================================

def save_to_csv(records, output_file=OUTPUT_FILE):
    """Save the extracted records to CSV."""

    with Path(output_file).open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(records)

    return Path(output_file)


# ==================================================
# COMMAND-LINE VERSION
# ==================================================

def main():
    print("=" * 50)
    print("          PYTHON WEB SCRAPER")
    print("=" * 50)

    try:
        pages = int(
            input("Number of catalog pages (1-10): ").strip()
        )

        records, message, pages_scraped = scrape_website(
            start_url=BASE_URL,
            max_pages=pages,
        )

        save_to_csv(records)

        print("\nAccess check:", message)
        print("Pages scraped:", pages_scraped)
        print("Books extracted:", len(records))
        print("CSV saved to:", OUTPUT_FILE)

        print("\nSample records:")

        for record in records[:5]:
            print(
                f"{record['title']} | "
                f"{record['price']} | "
                f"{record['product_url']}"
            )

    except (
        ValueError,
        PermissionError,
        requests.RequestException,
        OSError,
        csv.Error,
    ) as error:
        print(f"\nScraping failed: {error}")


if __name__ == "__main__":
    main()
