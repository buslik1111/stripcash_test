from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from uuid import uuid4


def build_unique_tracking_link(link: str) -> tuple[str, str]:
    """Add a unique sourceId and return the tracking URL with its source."""

    parsed_url = urlparse(link)
    query_params = dict(parse_qsl(parsed_url.query))
    source_id = f"qa{uuid4().hex}"
    query_params["sourceId"] = source_id

    tracking_link = urlunparse(parsed_url._replace(query=urlencode(query_params)))

    return tracking_link, source_id
