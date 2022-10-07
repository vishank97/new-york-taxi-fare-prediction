from fastapi import FastAPI
from pydantic import BaseModel
from taxi_fare import infer_model

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Spaceship Titanic model inference!"}

class TaxiFare(BaseModel):
    # name: str
    # description: Union[str, None] = None
    # price: float
    # tax: Union[float, None] = None

    pickup_datetime: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: float
    dropoff_longitude: float
    passenger_count: int

@app.post("/infer")
async def infer(tf: TaxiFare):
    return infer_model(
       tf.pickup_datetime,
       tf.pickup_latitude,
       tf.pickup_longitude,
       tf.dropoff_latitude,
       tf.dropoff_longitude,
       tf.passenger_count
    )