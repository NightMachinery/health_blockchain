from .block import Block
from .blockchain import Blockchain

from icecream import ic
from typing import Any
import dataclasses
import json
import base64

json_bytes_base64_marker = "bytes_base64_encoded_marker"
json_blockchain_marker = "json_blockchain_marker"
json_dataclass_marker = "json_dataclass_marker"


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Blockchain):
            return (json_blockchain_marker, o.blocks)
        elif dataclasses.is_dataclass(o):
            # class_name = o.__class__.__name__
            class_name = "NA"
            if isinstance(o, Block):
                class_name = "Block"
            else:
                return super().default(o)
            return (json_dataclass_marker, class_name, dataclasses.asdict(o))
        elif isinstance(o, bytes):
            return (json_bytes_base64_marker, base64.b64encode(o).decode("ascii"))
        else:
            return super().default(o)


def enhanced_json_decode_dict(decoded_dict, /):
    for k, v in decoded_dict.items():
        decoded_dict[k] = enhanced_json_decode_one(v)

    return decoded_dict


def enhanced_json_decode_one(o, /):
    # ic(o)

    if isinstance(o, dict):
        return enhanced_json_decode_dict(o)
    elif isinstance(o, list):
        o_lst = o
        if len(o_lst) in (2, 3):
            if o_lst[0] == json_bytes_base64_marker:
                return base64.b64decode(o_lst[1], validate=True)
            elif o_lst[0] == json_blockchain_marker:
                return Blockchain(
                    enhanced_json_decode_one(o_lst[1]))
            elif o_lst[0] == json_dataclass_marker:
                if o_lst[1] == "Block":
                    return Block(**enhanced_json_decode_one(o_lst[2]))
                else:
                    return o

        return list(map(enhanced_json_decode_one, o))
    else:
        return o


def json_dumps(obj, /):
    return json.dumps(obj, cls=EnhancedJSONEncoder)


def obj_deserialize(block_bytes, /):
    block_dict = json.loads(
        block_bytes,
        cls=json.JSONDecoder,
        # object_hook=enhanced_json_decode_one,
    )
    return enhanced_json_decode_one(block_dict)


block_deserialize = obj_deserialize


def obj_serialize(block: Any, /):
    return json_dumps(block).encode()


block_serialize = obj_serialize
