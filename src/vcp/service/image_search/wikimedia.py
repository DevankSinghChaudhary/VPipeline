import os
import re
import time
from html import unescape

import requests
from langgraph.types import Send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from vcp.schemas import WikimediaAsset
from vcp.state import GlobalState
from vcp.utils import root

API_URL = "https://commons.wikimedia.org/w/api.php"

HEADERS = {
    "User-Agent": "VPipeline/0.1 (https://github.com/devanksinghchaudhary/vpipeline)"
}

ALLOWED_MIME = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

DOWNLOAD_PATH = root.find() / "renderer/public/images"

# Global session for downloads with retry logic
download_session = requests.Session()
retry = Retry(
    total=5,
    connect=3,
    read=3,
    status=5,
    backoff_factor=1.0,
    status_forcelist={429, 500, 502, 503, 504},
    allowed_methods={"GET"},
    respect_retry_after_header=True,
)
adapter = HTTPAdapter(max_retries=retry)
download_session.mount("https://", adapter)
download_session.mount("http://", adapter)
download_session.headers.update(HEADERS)


def download_image(url: str, save_dir: str = DOWNLOAD_PATH, delay: float = 0.5) -> str:
    """
    Download an image from a direct URL and save it to a custom directory.
    Adds a delay between downloads to avoid rate limiting.

    Args:
        url: Direct URL of the image.
        save_dir: Custom directory to save the image (default: DOWNLOAD_PATH).
        delay: Delay in seconds between downloads (default: 1.0).

    Returns:
        Path to the downloaded image file, or an empty string if download fails.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Remove query parameters from the URL
    clean_url = url.split("?")[0]
    filename = os.path.basename(clean_url)
    filepath = os.path.join(save_dir, filename)

    try:
        # Add delay to avoid rate limiting
        time.sleep(delay)

        response = download_session.get(clean_url, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, "wb") as file:
            file.writelines(response.iter_content(1024))
        print(f"Downloaded: {filename}")
        return filepath
    except Exception as e:
        print(f"Failed to download {clean_url}: {e}")
        return ""


class WikimediaImageSearch:
    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            status=3,
            backoff_factor=0.5,
            status_forcelist={429, 500, 502, 503, 504},
            allowed_methods={"GET"},
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def search(self, query: str, limit: int = 1) -> list[WikimediaAsset]:
        query = query.strip()

        if not query:
            raise ValueError("Wikimedia search query cannot be empty.")

        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50.")

        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"file:{query}",
            "gsrnamespace": 6,
            "gsrlimit": limit,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiextmetadatafilter": "ImageDescription|Artist|Credit|LicenseShortName|UsageTerms|LicenseUrl",
            "format": "json",
            "formatversion": 2,
        }

        response = self.session.get(
            API_URL,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise RuntimeError(
                f"Wikimedia API error: {data['error'].get('info', 'Unknown error')}"
            )

        pages = data.get("query", {}).get("pages", [])

        assets = []
        seen_urls = set()

        for page in pages:
            asset = self._parse_page(page)

            if asset is None:
                continue

            if asset.url in seen_urls:
                continue

            seen_urls.add(asset.url)
            assets.append(asset)

        return assets

    def _parse_page(self, page: dict) -> WikimediaAsset | None:
        if page.get("ns") != 6:
            return None

        imageinfo = page.get("imageinfo")

        if not imageinfo:
            return None

        info = imageinfo[0]
        mime = info.get("mime")

        if mime not in ALLOWED_MIME:
            return None

        url = info.get("url")

        if not url:
            return None

        metadata = info.get("extmetadata", {})

        return WikimediaAsset(
            title=page.get("title", ""),
            url=url,
            thumburl=info.get("thumburl"),
            descriptionurl=info.get("descriptionurl"),
            width=info.get("width", 0),
            height=info.get("height", 0),
            mime=mime,
            description=self._metadata_value(metadata, "ImageDescription"),
            license=self._metadata_value(metadata, "LicenseShortName"),
            artist=self._metadata_value(metadata, "Artist"),
            credit=self._metadata_value(metadata, "Credit"),
            usage_terms=self._metadata_value(metadata, "UsageTerms"),
            license_url=self._metadata_value(metadata, "LicenseUrl"),
        )

    @staticmethod
    def _metadata_value(metadata: dict, key: str) -> str:
        value = metadata.get(key, {}).get("value", "")

        if not isinstance(value, str):
            return ""

        value = unescape(value)
        value = re.sub(r"<[^>]+>", " ", value)
        value = re.sub(r"\s+", " ", value)

        return value.strip()


def fanout_image(state: GlobalState):
    visual_response = state["visual"]

    return [
        Send("Image", {"query": query})
        for visual in visual_response.visual
        for segment in visual.segments
        for query in segment.classification.queries
    ]


def search_images(
    state,
    limit: int = 5,
    download: bool = True,
    save_dir: str = DOWNLOAD_PATH,
    delay: float = 0.2,
):
    query = state["query"]

    print(f"    [TOOL] Wikimedia Searched for {query}")

    images = WikimediaImageSearch().search(query, limit)

    result = {
        "images": [
            {
                "title": image.title,
                "description": image.description,
                "url": image.url,
                **(
                    {"local_path": download_image(image.url, save_dir, delay)}
                    if download
                    else {}
                ),
            }
            for image in images
        ]
    }

    return result
