from time import time_ns
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def build_unique_tracking_link(link: str) -> str:
    """Добавляет уникальный sourceId, чтобы tracking-система не склеила клик"""

    parsed_url = urlparse(link)
    query_params = dict(parse_qsl(parsed_url.query))
    query_params["sourceId"] = f"qa{time_ns()}"

    return urlunparse(parsed_url._replace(query=urlencode(query_params)))
