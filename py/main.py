from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

import uvicorn
import sys
import os

# TODO, to make this flexible when Vite change their port#, i.e. auto track port allowed list
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:4242",
    "http://localhost:5173",
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:4242",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:80",
    "http://127.0.0.1:8080",
]

with open('pid.txt', 'w') as f:
    f.write(str(os.getpid()))

def setPort():
    p:int = 4242
    try:
        p = int(sys.argv[1])
        print("info: assigned default port "+ str(p))  
    except:
        print("info: assigned default port 4242")   
    return p

def setReload():
    r: bool = False
    # TODO, later check if in dev and perform hot reload
    return r

app = FastAPI()
port = setPort()
reload = setReload()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root page
@app.get("/")
async def read_root():
    return {"status": "server is running", "docs": "go to /docs to get more info on API"}

# Get the python child of child pid, for kill instructions
@app.get("/pid")
def read_root():
    return {"pid": str(os.getpid())}


app.include_router(api_router)

if __name__ == "__main__":
    # uvicorn.run(app, host='127.0.0.1', port=port)
    uvicorn.run(app, host='127.0.0.1', port=port, log_level="info", reload=reload)
    print("running")