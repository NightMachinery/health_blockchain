import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, Union, List


@dataclass(frozen=True)
class Block:
    content_dictionary: Dict
    previous_block_hash: Union[bytes, None]
    signatures: List[bytes]


block_update = dataclasses.replace
