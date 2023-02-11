from fastapi import FastAPI

app = FastAPI()


@app.post("/signup")
async def signup():
    return


@app.post("/login")
async def login():
    return
