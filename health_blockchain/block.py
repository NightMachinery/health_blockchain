from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class Block:
    signature: Any
    content_dictionary: Dict
