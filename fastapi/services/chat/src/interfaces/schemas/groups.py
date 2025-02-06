from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .permissions import PermissionRead


class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    permissions: List[int] = []


class GroupId(BaseModel):
    id: int


class GroupRead(GroupBase):
    permissions: List[PermissionRead] = []

    model_config = ConfigDict(extra="ignore")


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase, GroupId):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    permissions: Optional[List[int]] = None


class GroupDelete(GroupId):
    pass
