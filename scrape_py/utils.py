from urllib.parse import urljoin, urlsplit
from typing import TypedDict
from bs4 import BeautifulSoup, Tag


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(input_url: str):
    splits = urlsplit(input_url)
    return f"{splits.netloc}{splits.path}"


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1")
    h2_tag = soup.find("h2")
    h1_tag_Val = h1_tag.get_text(strip=True) if isinstance(h1_tag, Tag) else ""
    h2_tag_Val = h2_tag.get_text(strip=True) if isinstance(h2_tag, Tag) else ""
    if h1_tag_Val != "":
        return h1_tag_Val
    elif h2_tag_Val != "":
        return h2_tag_Val
    else:
        return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")
    if main_tag is not None:
        p_tag = main_tag.find("p")
        return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
    p_tag = soup.find("p")
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    anchor_tags = soup.find_all("a")
    url_collection = []
    for tag in anchor_tags:
        url = tag.get("href", default="")
        if url == "":
            continue
        complete_url = urljoin(base_url, url)
        url_collection.append(complete_url)
    return url_collection


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.find_all("img")
    url_collection = []
    for tag in image_tags:
        url = tag.get("src", default="")
        if url == "":
            continue
        complete_url = urljoin(base_url, url)
        url_collection.append(complete_url)
    return url_collection


def extract_page_data(html: str, page_url: str):
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    links = get_urls_from_html(html, page_url)
    image_links = get_images_from_html(html, page_url)

    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": links,
        "image_urls": image_links,
    }
