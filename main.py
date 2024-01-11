from fastapi import FastAPI
from web import advertisements_web
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(advertisements_web.router)
app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=5000)
