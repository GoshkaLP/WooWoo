from fastapi import FastAPI
from views import status, users, forms, feed


app = FastAPI()
app.include_router(status)
app.include_router(users)
app.include_router(forms)
app.include_router(feed)
