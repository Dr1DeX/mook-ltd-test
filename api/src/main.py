from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.dispatcher.users.auth.handlers import router as auth_router
from src.dispatcher.users.handlers import router as user_router

app = FastAPI(title='API LTD Stargazer')

app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
