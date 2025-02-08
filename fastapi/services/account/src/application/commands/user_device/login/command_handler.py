from src.application import CommandHandler, command_reg
from src.domain.models import UserDevice
from src.domain.services.user_device import UserDeviceService

from .command import LoginUserDevice


@command_reg.register(LoginUserDevice)
class LoginUserDeviceHandler(CommandHandler[LoginUserDevice]):
    async def handle(self, command, session) -> None:
        device = UserDevice(
            **{
                UserDevice.device_type.name: command.device_type,
                UserDevice.operating_system.name: command.operating_system,
                UserDevice.browser_type.name: command.browser_type,
                UserDevice.ip_address.name: command.ip_address,
                UserDevice.user_id.name: command.user_id,
                UserDevice.device_id.name: UserDeviceService.build_device_id(
                    ip_address=command.ip_address,
                    user_id=command.user_id,
                    device_type=command.device_type,
                    operating_system=command.operating_system,
                ),
            }
        )
        await session.merge(device)
