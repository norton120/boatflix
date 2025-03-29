from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
#from webapp.api import router as api_router
from webapp.web import router as web_router

app = FastAPI()

# Mount static files directory
app.mount("/assets", StaticFiles(directory="webapp/assets"), name="assets")
app.mount("/assets/services", StaticFiles(directory="webapp/assets/services"), name="services")

#app.include_router(api_router)
app.include_router(web_router)

@app.get("/health")
async def healthcheck():
    return {"message": "success"}
