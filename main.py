from fastapi import FastAPI

app = FastAPI()

if __name__ == 'main':
    import uvicorn
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8500)
