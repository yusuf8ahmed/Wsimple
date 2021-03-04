# errors
from .errors import InvalidAccessTokenError, WealthsimpleServerError
# 3 party
from requests import request
from loguru import logger
from box import Box

def requestor(endpoint, args, **kwargs):
    name = endpoint.name
    url = endpoint.value.route.format(**args)
    logger.debug("{} called".format(name))
    r = request(
            endpoint.value[1], 
            url,
            **kwargs
    )
    logger.debug("{}: {}".format(name, r.status_code))
    if r.status_code == 401:
        raise InvalidAccessTokenError
    elif r.status_code >= 500:
        raise WealthsimpleServerError
    else:
        return Box(r.json())