from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
import uvicorn
from model import update_database, add_image

app = FastAPI()

count = 1



@app.get("/PING")
async def root():
    return {"message" : "PONG"}

@app.post("/file")
async def upload_image(image : UploadFile):
    file = image.file
    filename = f"{count}_{image.filename}"
    with open(filename, "wb") as img:
        img.write(file.read())
    await update_database()
    await add_image(filename)
    return {"status_code" : 200}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)