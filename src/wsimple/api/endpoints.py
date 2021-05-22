from enum import Enum
from typing import NamedTuple


class Route(NamedTuple):
    """ Route: holds the route and method to access a resource on Wealthsimple"""

    route: str
    method: str


class Endpoints(Enum):
    BASE = "https://trade-service.wealthsimple.com/"
    BASE_PUBLIC = "https://trade-service.wealthsimple.com/public/"
    BASE_STATUS = "https://status.wealthsimple.com/"

    LOGIN = Route("{base}auth/login", "POST")
    REFRESH = Route("{base}auth/refresh", "POST")

    GET_ME = Route("{base}me", "GET")
    GET_ACCOUNT = Route("{base}account", "GET")
    GET_ACCOUNT_LIST = Route("{base}account/list", "GET")
    GET_ACCOUNT_HISTORY = Route("{base}account/history/{time}", "GET")
    GET_PERSON = Route("{base}person", "GET")
    GET_BANK_ACCOUNTS = Route("{base}bank-accounts", "GET")
    GET_POSITONS = Route("{base}account/positions", "GET")

    GET_ORDERS = Route("{base}orders", "GET")
    SEND_ORDER = Route("{base}orders", "POST")
    CANCEL_ORDER = Route("{base}orders/{order_id}", "DELETE")

    FIND_SECURITIES = Route("{base}securities", "GET")
    FIND_SECURITIES_BY_ID = Route("{base}securities/{security_id}", "GET")
    FIND_SECURITIES_HISTORY = Route(
        "{base}securities/{security_id}/historical_quotes/{time}", "GET"
    )

    GET_ACTIVITES = Route("{base}account/activities", "GET")

    MAKE_WITHDRAWALS = Route("{base}withdrawals", "POST")
    GET_WITHDRAWAL_BY_ID = Route("{base}withdrawals/{funds_transfer_id}", "GET")
    LIST_WITHDRAWALS = Route("{base}withdrawals", "GET")
    DELETE_WITHDRAWAL_BY_ID = Route("{base}withdrawals/{funds_transfer_id}", "DELETE")

    MAKE_DEPOSITS = Route("{base}deposits", "POST")
    GET_DEPOSIT_BY_ID = Route("{base}deposits/{funds_transfer_id}", "GET")
    LIST_DEPOSITS = Route("{base}deposits", "GET")
    DELETE_DEPOSIT_BY_ID = Route("{base}deposits/{funds_transfer_id}", "DELETE")

    GET_ALL_MARKETS = Route("{base}markets", "GET")

    GET_WATCHLIST = Route("{base}watchlist", "GET")
    ADD_TO_WATCHLIST = Route("{base}watchlist/{security_id}", "PUT")
    DELETE_FROM_WATCHLIST = Route("{base}watchlist/{security_id}", "DELETE")

    GET_EXCHANGE_RATE = Route("{base}forex", "GET")

    GET_FACT_SHEET = Route("{base}fact-sheets", "GET")

    GET_TOP_MARKET_MOVERS = Route("{base}securities/top_market_movers", "GET")
    GET_MOST_WATCHED = Route("{base}securities/most_watched", "GET")
    GET_FEATURED = Route("{base}security-groups/featured", "GET")
    GET_SECURITIES_IN_GROUPS = Route(
        "{base}security-groups/{group_id}/securities", "GET"
    )
    GET_ALL_GROUPS = Route("{base}security-groups", "GET")

    GET_MOBILE_DASHBOARD = Route("{base}mobile-dashboard", "GET")

    GET_GLOBAL_ALERTS = Route("{base}global-alerts", "GET")
    GET_USER_ALERTS = Route("{base}global-alerts/user", "GET")

    GET_SUPPORTED_INTERNAL_TRANSFERS = Route(
        "{base}supported-internal-transfers", "GET"
    )
    CREATE_INTERNAL_TRANSFER = Route("{base}internal_transfers", "POST")

    GET_TAX_DOCUMENTS = Route("{base}tax-documents", "GET")

    GET_MONTHLY_STATEMENTS = Route("{base}monthly-statements", "GET")
    GET_URL_MONTHLY_STATEMENTS = Route(
        "{base}monthly-statements/{pdf_statement_id}", "GET"
    )

    GET_WEBSOCKET_URI = Route("{base}websocket-ticket", "POST")

    PUBLIC_GET_SECURITIES_BY_TICKER = Route("{base}securities/{ticker}", "GET")
    PUBLIC_GET_SECURITIES_HISTORICAL = Route(
        "{base}securities/{ticker}/historical_quotes/{time}", "GET"
    )
    PUBLIC_GET_TOP_TRADED = Route("{base}securities/top_traded", "GET")
    PUBLIC_GET_SECURITIES_NEWS = Route("{base}securities/{ticker}/news", "GET")

    GET_SUMMARY_STATUS = Route("{base}api/v2/summary.json", "GET")
    GET_CURRENT_STATUS = Route("{base}api/v2/status.json", "GET")
    GET_HISTORICAL_STATUS = Route("{base}api/v2/incidents.json", "GET")
