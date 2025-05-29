from typing import TypedDict, Optional, List

class AccessibilityScanState(TypedDict):
    url: str
    scan_results: Optional[dict]
    errors: Optional[List[str]]