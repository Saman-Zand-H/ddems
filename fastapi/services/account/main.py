from src.infrastructure.auth.user_manager import get_user_db
from src.interfaces.endpoints import router

from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(get_user_db)])
app.include_router(router)
