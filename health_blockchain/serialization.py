from .block import Block

import dataclasses
import json
import base64

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            elif isinstance(o, bytes):
                return base64.b64encode(o).decode('ascii')
            else:
                return super().default(o)


def json_dumps(obj):
    return json.dumps(obj, cls=EnhancedJSONEncoder)



def block_deserialize(block_bytes):
    #: @todo0
    ##
    block_dict = json.loads(block_bytes)
    return Block(**block_dict)


def block_serialize(block: Block):
    #: @todo0
    ##
    return json_dumps(block)
