from database import database
from fastapi import FastAPI
from routers.user import router as user_router
from routers.auth import router as auth_router
from routers.transaction import router as transaction_router

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(transaction_router)
