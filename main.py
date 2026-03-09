import logging
import  shutil
from fastapi import FastAPI, File, UploadFile
import uvicorn
from model import update_database, add_image
from pathlib import Path
import os
from arq import  create_pool
from arq.connections import RedisSettings

app = FastAPI()

DIR = Path(__file__).parent

count = 1

async def add_task(id):
    redis = await create_pool(RedisSettings(host="localhost", port=6379))
    task = await redis.enqueue_job('new_photo', id)
    result = await task.result()
    logging.info(result)
    await redis.close

@app.get("/PING")
async def root():
    return {"message" : "PONG"}

@app.post("/file")
async def upload_image(image : UploadFile):
    global count
    file = image.file
    filename = f"{count}_{image.filename}"
    with open(filename, "wb") as img:
        img.write(file.read())
    shutil.move(filename, "../smart-birdy/birds")
    file_address = os.path.abspath(f"/birds/{filename}")
    await update_database()
    await add_image(filename, file_address)
    await add_task(count)
    count += 1
    return {"status_code" : 200}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)