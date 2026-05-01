from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None
