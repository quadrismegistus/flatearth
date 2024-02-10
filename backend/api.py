from flatearth import *

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define a list of allowed origins for CORS
# You can use "*" to allow all origins or specify only the ones you need
origins = [
    "http://localhost:8100",  # Assuming your React app runs on this port
    "http://localhost:3000",  # Commonly used port for React development
    # Add any other origins you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/place/{lat}/{lon}")
async def get_place(lat: float, lon: float):
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    print(get_place,lat,lon)
    # Here you can add logic to process latitude and longitude, 
    # like querying a database or calling an external API.
    place=Place.locate(lat=lat, lon=lon)
    return place.data if place else {}


from pydantic import BaseModel
from typing import List

class PostQuery(BaseModel):
    type: str
    seen: List[int]

@app.post("/posts/query")
async def get_posts(query:PostQuery):
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    logger.debug(query)
    df = post_map_df(seen=query.seen).rename(columns={'html':'content'})
    return df[['id','lat','lon','content']].to_dict('records')

@app.get("/posts/latest")
async def get_posts():
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    df = post_map_df().rename(columns={'html':'content'})
    return df[['id','lat','lon','content']].sort_values(['lon','lat']).to_dict('records')