from fastapi import FastAPI
from src.dispatcher.users.handlers import router as user_router
from src.dispatcher.users.auth.handlers import router as auth_router


app = FastAPI(title='API LTD Stargazer')
app.include_router(user_router)
app.include_router(auth_router)
