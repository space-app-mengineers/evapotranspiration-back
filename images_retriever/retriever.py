from PIL import Image
import requests
import ee
from fastapi import FastAPI, HTTPException

import requests


def init_ee():
    # Initialize Earth Engine
    try:
        ee.Authenticate(quiet=True)
        ee.Initialize()
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        # You might want to handle this error more gracefully in a production environment

def get_ee_image(lat: float, lon: float) -> bytes:
    roi = ee.Geometry.Point([-70.56, -33.52])
    landsat = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA") \
                .filterDate('2024-01-24', '2024-03-24')\
                .filterBounds(roi)
    
    image = landsat.median().select(['B4', 'B3', 'B2'])

    region = roi.buffer(10000).bounds().getInfo()

    url = image.getThumbUrl({
        'region': region['coordinates'],
        'dimensions': 512,
        'format': 'png',
        'min': 0,
        'max': 0.3,
        'format': 'png'
    })

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download image from Earth Engine")
    return response.content

def get_polygon_image(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> bytes:

    print("hola")
    x_c = (x1 + x2 + x3 + x4) / 4
    y_c = (y1 + y2 + y3 + y4) / 4
    roi_center = [x_c, y_c]

    # Define a bounding box (coordinates: [min_lon, min_lat, max_lon, max_lat])
    polygon = ee.Geometry.Polygon([[-70.6483, -33.4569],
        [-70.6483, -33.4469],
        [-70.6383, -33.4469],
        [-70.6383, -33.4569],
        [-70.6483, -33.4569]])

    landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
            .filterDate('2023-01-01', '2023-12-31') \
            .filterBounds(polygon) \
            # .sort('CLOUD_COVER')

    # Select the least cloudy image
    # image = landsat.first()

    image = landsat.median().select(['B4', 'B3', 'B2'])

    region = polygon.buffer(100).bounds().getInfo()

    print(image.getInfo())
    url = image.getThumbUrl({
        'region': polygon,
        'dimensions': 512,
        'format': 'png',
        'min': 0,
        'max': 0.3
    })

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download image from Earth Engine")

    # Return the image file
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download image from Earth Engine")

    return response.content

def get_asd():
    import ee
    import geeet
    import geemap
    import geemap.colormaps as cm
    from geeet.eepredefined import landsat

    region = dict(type="Point", coordinates=[-70.646652, -33.605887])  # Santiago, Chile

    # Define a custom workflow (TSEB model + LE extrapolation)
    workflow = [
        geeet.tseb.tseb_series,
        landsat.extrapolate_LE    # this adds the "ET" band, in mm/day
    ]

    landsat_era5_tseb_collection = landsat.mapped_collection(
        workflow,
        date_start = "2024-04-01",
        date_end = "2024-08-01",
        region = region, 
        era5 = True,
        timeZone="America/Santiago" # the time property will be set in local time (UTC -3 for this example)
    )
    # Select one image by LANDSAT_INDEX:
    image = (
        landsat_era5_tseb_collection
        .filter(ee.Filter.eq("LANDSAT_INDEX", 
        landsat_era5_tseb_collection.aggregate_array("LANDSAT_INDEX").getInfo()[0]
        ))
        .first()
        .clip(
            ee.Geometry(region)
            .buffer(1000)   # area around the point in meters
            .bounds()        
        )
    )


    et = image.select('ET')
    filename="et_image.png"
    geemap.ee_export_image(et, filename="et_image.png", scale=30, region=ee.Geometry(region).buffer(1000).bounds(), file_per_band=False)
    return filename