from fastapi import FastAPI
#from webapp.api import router as api_router
from webapp.web import router as web_router

app = FastAPI()

#app.include_router(api_router)
app.include_router(web_router)

@app.get("/health")
async def healthcheck():
    return {"message": "success"}
