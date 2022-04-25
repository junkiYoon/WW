from fastapi import FastAPI

import uvicorn

from src.apps import api_router


app = FastAPI()
app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
