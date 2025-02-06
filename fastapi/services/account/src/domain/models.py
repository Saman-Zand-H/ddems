import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


group_permission = sa.Table(
    "group_permission_association",
    Base.metadata,
    sa.Column("group_id", sa.ForeignKey("groups.id", ondelete="CASCADE")),
    sa.Column("permission_id", sa.ForeignKey("permissions.id", ondelete="CASCADE")),
)

user_group = sa.Table(
    "user_group_association",
    Base.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("group_id", sa.ForeignKey("groups.id", ondelete="CASCADE")),
)

user_permission = sa.Table(
    "user_permission_association",
    Base.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("permission_id", sa.ForeignKey("permissions.id", ondelete="CASCADE")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    username = sa.Column(sa.String(255), unique=True, nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    last_name = sa.Column(sa.String(50), nullable=False)
    last_login = sa.Column(sa.DateTime(timezone=True), nullable=True)
    date_joined = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

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
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

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
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)
    code = sa.Column(sa.String(255), unique=True, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

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
