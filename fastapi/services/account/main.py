from config import settings  # noqa
from utils import autodiscover
from src.interfaces.dependencies import (
    get_command_registry,
    get_query_registry,
    get_uow,
)
from src.interfaces.api import router

from fastapi import Depends, FastAPI

autodiscover("src.application.commands", "command_handler.py")
autodiscover("src.application.queries", "query_handler.py")

app = FastAPI(
    dependencies=[
        Depends(get_uow),
        Depends(get_query_registry),
        Depends(get_command_registry),
    ]
)
app.include_router(router)
