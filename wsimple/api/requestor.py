import json
# errors
from .errors import InvalidAccessTokenError, WealthsimpleServerError, RouteNotFoundException
# 3 party
from requests import request
from loguru import logger
from box import Box

def requestor(endpoint, args, request_status=False, response_list=False, **kwargs):
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
    if r.status_code == 404:
        print(r.url)
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