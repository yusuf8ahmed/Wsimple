import json

# errors
from .errors import (
    InvalidAccessTokenError,
    WealthsimpleServerError,
    RouteNotFoundException,
)

# 3 party
import cloudscraper as req
from loguru import logger
from box import Box


def requestor(
    endpoint,
    args,
    logger=None,
    request_status=False,
    response_list=False,
    login_refresh=False,
    **kwargs,
) -> Box:
    name: str = endpoint.name
    url: str = endpoint.value.route.format(**args)
    rcloud = req.create_scraper()
    logger.debug("{} called".format(name))
    r = rcloud.request(method=endpoint.value[1], url=url, **kwargs)
    logger.debug("{}: {}".format(name, r.status_code, r.url))
    if login_refresh:
        return r
    if r.status_code == 401:
        raise InvalidAccessTokenError
    elif r.status_code == 404:
        logger.error(f"404 on {r.url}")
        raise RouteNotFoundException
    elif r.status_code >= 500:
        raise WealthsimpleServerError
    else:
        if request_status:
            return Box(json.loads(r.content))
        elif response_list:
            return Box(r.json()[0])
        else:
            return Box(r.json())
