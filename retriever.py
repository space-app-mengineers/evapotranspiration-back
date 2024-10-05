# import os
# from io import BytesIO
# from skimage import io
# import requests
# import json
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import cartopy.crs as ccrs
# import cartopy
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import urllib.request
# import urllib.parse
# import mapbox_vector_tile
# import xml.etree.ElementTree as xmlet
# import lxml.etree as xmltree
# from PIL import Image as plimg
# import numpy as np
# from owslib.wms import WebMapService
# from IPython.display import Image, display

import requests
import json
import os

# URL de la API de AppEEARS
url = "https://appeears.earthdatacloud.nasa.gov/api/task"

# Autenticación (debes usar tu token de NASA Earthdata)
headers = {
    "Authorization":  "Bearer eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ", 
}

# Definir los parámetros de la solicitud
payload = {
    "task_type": "point",  # tipo de tarea, puede ser "area" o "point"
    "params": {
        "startDate": "2023-01-01",  # Fecha de inicio
        "endDate": "2023-09-30",    # Fecha de fin
        "layers": [
            {
                "layer": "HLSL30.v002.Reflectance.B01",  # Especifica la capa de HLSL30 v002
                "product": "HLSL30.v002"  # Producto HLS
            }
        ],
        "coordinates": [-100.445882, 39.783730],  # Ejemplo de coordenadas (longitud, latitud)
    },
    "output": {
        "format": {
            "type": "csv"  # Formato de salida
        }
    }
}

# Enviar la solicitud POST
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Ver el resultado de la solicitud
if response.status_code == 200:
    task_id = response.json().get('task_id')
    print(f"Tarea creada exitosamente, ID de la tarea: {task_id}")
else:
    print(f"Error en la solicitud: {response.status_code}")
    print(response.text)
