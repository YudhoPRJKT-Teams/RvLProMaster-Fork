from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class BotsData:
  raw_json: Optional[dict[str, Any]] = None
  status_code: Optional[int] = None
  serialize_json: Optional[str] = None