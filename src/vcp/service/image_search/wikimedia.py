import requests

from vcp.schemas import WikimediaAsset


API_URL = "https://commons.wikimedia.org/w/api.php"

HEADERS = {
    "User-Agent": "VPipeline/0.1 (example@gmail.com)"
}

ALLOWED_MIME = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def search_images(query: str, limit: int = 20):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"file:{query}",
        "gsrnamespace": 6,
        "gsrlimit": limit,

        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1920,

        "format": "json",
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=20,
    )

    response.raise_for_status()

    return response.json()


def parse_page(page):
    if page.get("ns") != 6:
        return None

    info_list = page.get("imageinfo")

    if not info_list:
        return None

    info = info_list[0]

    if info.get("mime") not in ALLOWED_MIME:
        return None

    metadata = info.get("extmetadata", {})

    description = (
        metadata
        .get("ImageDescription", {})
        .get("value", "")
    )

    license_name = (
        metadata
        .get("LicenseShortName", {})
        .get("value", "")
    )

    return {
        "title": page.get("title"),
        "url": info.get("url"),
        "thumburl": info.get("thumburl"),
        "descriptionurl": info.get("descriptionurl"),
        "width": info.get("width"),
        "height": info.get("height"),
        "mime": info.get("mime"),
        "description": description,
        "license": license_name,
    }


if __name__ == "__main__":
    data=input("Enter: ")
    data = search_images(data)

    pages = data.get("query", {}).get("pages", {})

    assets = []

    for page in pages.values():
        asset = parse_page(page)

        if asset is not None:
            assets.append(asset)

    for asset in assets:
        print(asset)
