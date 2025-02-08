import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import UniqueConstraint

from src.domain.choices import DeviceType


class Base(DeclarativeBase):
    pass


class UserDevice(Base):
    __tablename__ = "user_devices"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    device_id = sa.Column(sa.Text, nullable=False)
    device_type = sa.Column(sa.Enum(DeviceType), nullable=True)
    operating_system = sa.Column(sa.String(100), nullable=True)
    browser_type = sa.Column(sa.String(100), nullable=True)
    ip_address = sa.Column(sa.String(45), nullable=True)
    last_login = sa.Column(sa.DateTime, insert_default=sa.func.now())

    __table_args__ = (UniqueConstraint("device_id", "user_id", name="uq_device_user"),)
