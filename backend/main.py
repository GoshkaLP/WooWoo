from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from views import status, users, forms, feed


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status)
app.include_router(users)
app.include_router(forms)
app.include_router(feed)
