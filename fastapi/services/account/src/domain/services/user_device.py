from src.domain.choices import DeviceType


class UserDeviceService:
    @staticmethod
    def build_device_id(
        ip_address: str,
        user_id: int,
        device_type: DeviceType = None,
        operating_system: str = None,
    ):
        return f"{ip_address}-{user_id}-{device_type}-{operating_system}"
