from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokensBox:
    """ TokenBox: holds the route and method to access a resource on Wealthsimple"""

    access_token: str
    refresh_token: str
    access_expires: datetime

    @property
    def tokens(self) -> List[Dict[str, str]]:
        return [
            {"Authorization": self.access_token},
            {"refresh_token": self.refresh_token},
        ]
