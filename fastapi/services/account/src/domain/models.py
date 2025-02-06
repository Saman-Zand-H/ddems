from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


group_permission = Table(
    "group_permission_association",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id", ondelete="CASCADE")),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE")),
)

user_group = Table(
    "user_group_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("group_id", ForeignKey("groups.id", ondelete="CASCADE")),
)

user_permission = Table(
    "user_permission_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())

    groups = relationship(
        "Group",
        secondary=user_group,
        back_populates="users",
        cascade="all, delete",
        passive_deletes=True,
    )
    permissions = relationship(
        "Permission",
        secondary=user_permission,
        back_populates="users",
        cascade="all, delete",
        passive_deletes=True,
    )

    group_names = association_proxy("groups", "name")
    permission_names = association_proxy("permissions", "name")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship(
        "User",
        secondary=user_group,
        back_populates="groups",
        cascade="all, delete",
        passive_deletes=True,
    )
    permissions = relationship(
        "Permission",
        secondary=group_permission,
        back_populates="groups",
        cascade="all, delete",
        passive_deletes=True,
    )

    user_usernames = association_proxy("users", "username")
    permission_names = association_proxy("permissions", "name")


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    code = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship(
        "User",
        secondary=user_permission,
        back_populates="permissions",
        cascade="all, delete",
        passive_deletes=True,
    )
    groups = relationship(
        "Group",
        secondary=group_permission,
        back_populates="permissions",
        cascade="all, delete",
        passive_deletes=True,
    )

    user_usernames = association_proxy("users", "username")
    group_names = association_proxy("groups", "name")
