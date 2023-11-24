from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()

class Image2VidSchema(BaseModel):
    """Models updatable field of a user profile"""
    data:list[str]

@app.post("/image2vid", response_model=dict)
def update_profile(payload:Image2VidSchema):
    for i,picture in enumerate(payload.data):
        data_split = picture.split('base64,')
        encoded_data = data_split[1]
        data = base64.b64decode(encoded_data)
        with open(f"uploaded_image{i}.png", "wb") as writer:
            writer.write(data)

    return {"detail": "OK"}

# Run ffmpeg command to convert images to video asynchonously
import subprocess
import asyncio
import os
import re

async def run_ffmpeg():
    command = "ffmpeg -framerate 1/3 -pattern_type glob -i '*.png' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stderr.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


# Create health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
