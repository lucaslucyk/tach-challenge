from typing import List, Optional, Tuple
from accounts.schemas.base import BaseModel


class PaginateParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort: Optional[List[Tuple[str, int]]] = None