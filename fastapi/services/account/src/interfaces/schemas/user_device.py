from pydantic import BaseModel


class UserDeviceId(BaseModel):
    device_id: str


class UserDeviceLogin(BaseModel):
    user_id: int
