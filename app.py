from fastapi import FastAPI, APIRouter
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Dict

import src.routers as routers

load_dotenv()
app: FastAPI = FastAPI()

routers_to_include: list[APIRouter] = [routers.moeda_router]
for rout in routers_to_include:
    app.include_router(rout)

@app.get('/')
def hello() ->  Dict[str, str]:
    return {'message': 'Hello, World!'}

def main() -> None:
    host: str = os.environ.get('HOST')
    port: int = int(os.environ.get('PORT'))
    uvicorn.run('app:app', host=host, port=port, reload=True)

if __name__ == '__main__':
    main()