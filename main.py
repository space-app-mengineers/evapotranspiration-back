from fastapi import FastAPI, HTTPException
from images_retriever import retriever
from fastapi.responses import FileResponse
import os
import tempfile

app = FastAPI()

retriever.init_ee()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get-image/{lat}/{lon}")
async def get_image(lat: float, lon: float):
    try:
        image_data = retriever.get_ee_image(lat, lon)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_data)
            temp_file_path = temp_file.name

        # Return the image file
        return FileResponse(temp_file_path, media_type="image/png", filename="earth_engine_image.png")
        # return get_ee_image(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/get-polygon-image/{x1}/{y1}/{x2}/{y2}/{x3}/{y3}/{x4}/{y4}")
async def get_polygon_image(
            x1: float, y1: float,
            x2: float, y2: float,
            x3: float, y3: float,
            x4: float, y4: float):
    try:
        image_data = retriever.get_polygon_image(x1, y1, x2, y2, x3, y3, x4, y4)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_data)
            temp_file_path = temp_file.name

        # Return the image file
        return FileResponse(temp_file_path, media_type="image/png", filename="earth_engine_image.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
