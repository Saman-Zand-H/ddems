from typing import Optional

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)


class PermissionId(BaseModel):
    id: int


class PermissionRead(PermissionBase, PermissionId):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionId):
    code: Optional[str] = Field(None, min_length=1, max_length=255)
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class PermissionDelete(PermissionId):
    pass
