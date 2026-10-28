from typing import Dict, List
from ..core.exceptions import UnknownCodeException
from .location import Location


class LocationRegistry:
    def __init__(self, locations: List[Location]) -> None:
        self._locations: Dict[str, Location] = {loc.get_code(): loc for loc in locations}

    def get(self, code: str) -> Location:
        location = self._locations.get(code)
        if not location:
            raise UnknownCodeException("Локация", code)
        return location

    def get_all(self) -> List[Location]:
        return list(self._locations.values())