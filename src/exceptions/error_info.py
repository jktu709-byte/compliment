from dataclasses import dataclass, field
from typing import Any


@dataclass
class Error_Context:
    req_id:int
    path:str
    method:str
    user_id:int
    extra:dict[str,Any] = field(default_factory=dict)
    
@dataclass    
class Error_Info:
    code:str
    public_msg:str
    status_code:int|None
    expose_to_client:bool
    expose_to_dev:bool
    original:Exception
    context:Error_Context