from typing import Optional

from src.application import Command
from src.domain.choices import DeviceType


class LoginUserDevice(Command):
    device_type: Optional[DeviceType] = None
    operating_system: Optional[str] = None
    browser_type: Optional[str] = None
    ip_address: str
    user_id: int
